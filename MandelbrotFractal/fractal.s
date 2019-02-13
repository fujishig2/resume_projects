calculate_escape:
########################################################################
#Author: Kyle Fujishige
#Date: October 5, 2017	
#
# Given a starting imaginary number (x_0) and a starting real number
# (y_0), set x = x_0 and y = y_0 and continuously check to see if the
# square of both the numbers is less than 4, while it is less than 4,
# make x = x^2 - y^2 + x_0 and y = 2*x*y + y_0, and check to see if
# x^2 + y^2 < 4 again. Continuously do this operation until x^2 + y^2
# is greater than or equal to 4, or until the max iterations is reached.
# If the max iterations is reached, this function will return $v0 as 0
# and $v1 as the max iterations. Otherwise $v0 is 1 and $v1 is the # of
# iterations.
#
# Arguments:
# $a0 = max number of iterations
# x_0 = initial real value (double)
# y_0 = initial imaginary value (double)
#
#	
# Returns
# $v0 = has escaped (1 if it escaped before the max iterations)
# $v1 = number of iterations algorithm went through
#	
#
# Register Usage
# $f4 = x_0
# $f6 = y_0
# $f8 = x
# $f10 = y
# $t0 = iterations	
# $f16 = temporary register used for various instructions
# $f18 = temporary register used for various instructions
# $t1 = temporary register used for various instructions
########################################################################

        #x_0 = $f4
        la 	$a2, x_0
        l.d 	$f4, 0($a2)

        #y_0 = $f6
        la 	$a2, y_0
        l.d 	$f6, 0($a2)

        #x = $f8
        mtc1.d 	$0, $f8
        cvt.d.w $f8, $f8

        #y = $f10
        mtc1.d 	$0, $f10
        cvt.d.w $f10, $f10

        #iterations = $t0
        addi 	$t0, $0, -1

        #go to max if iterations = max
loop:   bge	$t0, $a0, max

	#iterations += 1
	addi	$t0, $t0, 1

        #xtemp = x*x - y*y + x0
        mul.d 	$f16, $f8, $f8
        mul.d 	$f18, $f10, $f10
        sub.d 	$f16, $f16, $f18
        add.d 	$f16, $f16, $f4

        #y = 2*x*y + y0
        addi 	$t1, $0, 2
        mtc1.d 	$t1, $f18
        cvt.d.w $f18, $f18
        mul.d 	$f10, $f10, $f18
        mul.d 	$f10, $f10, $f8
        add.d 	$f10, $f10, $f6

        #x = xtemp
        sub.d 	$f18, $f18, $f18
        add.d 	$f8, $f16, $f18

        
        #branch to loop if x*x + y*y < 4
        mul.d 	$f16, $f8, $f8
        mul.d 	$f18, $f10, $f10
        add.d 	$f16, $f16, $f18
        addi 	$t1, $0, 4
        mtc1.d 	$t1, $f18
        cvt.d.w $f18, $f18
        c.lt.d 	$f16, $f18
        bc1t 	loop

        #return values and exit
        addi 	$v0, $0, 1
        add 	$v1, $t0, $0
        j 	exit

max:    add 	$v0, $0, $0
        add 	$v1, $a0, $0

exit:   jr 	$ra



	
.text
set_size:
########################################################################
#Author: Kyle Fujishige
#Date: October 5, 2017	
#
# Using the values inputted to $f12-$18, which contain the dimensions,
# subtract the max from the min from each axis, and divide it by the
# number of rows or columns being rendered, depending on which axis.
# That number will be the step size given to represent the real and
# imaginary spacing between each coordinate in GLIM. 	
#
# Arguments:
# $f12 = max imaginary value, set max_i to this value.
# $f14 = minimum imaginary value
# $f16 = max real value being rendered
# $f18 = minimum real value, set min_r to this value.
# $a0 = number of rows
# $a1 = number of columns	
#
#	
# Returns
# None
#	
#
# Register Usage
# $f6, $f8, $f10 = temporary registers used for various instructions
# $a2 = temporary register used for addresses.	
########################################################################

	#max_i = $f12
        la 	$a2, max_i
        s.d 	$f12, 0($a2)

	#min_r = $f18
        la 	$a2, min_r
        s.d 	$f18, 0($a2)

	#$f6 = (max_i - min_i)/rows
        sub.d 	$f8, $f12 $f14
        mtc1.d 	$a0, $f10
        cvt.d.w $f12, $f10
        div.d 	$f6, $f8, $f12

	#step_i = $f6
        la 	$a2, step_i
        s.d 	$f6, 0($a2)

	#$f6 = (max_r - min_r)/columns
        sub.d 	$f8, $f16, $f18
        mtc1.d 	$a1, $f10
        cvt.d.w $f12, $f10
        div.d 	$f6, $f8, $f12

	#step_r = $f6
        la 	$a2, step_r
        s.d 	$f6, 0($a2)

        jr 	$ra



.text
render:
########################################################################
#Author: Kyle Fujishige
#Date: October 5, 2017	
#
# Scan the entire display, coordinate at a time, and check to see where 
# the coordinate falls in the complex plane by running map_coords. Once
# the point is found, check to see if the point is within the mandelbrot
# set by calling calculate_escape. Depending when when it escaped, the
# modulo of the iterations with the pallet size will determine the color
# and symbol should be printed onto the screen using GLIM. If it reached
# the max iterations, then it is within the mandelbrot set, and the
# default symbol/color is used.	
#
# Arguments:
# $a0 = Rows
# $a1 = Columns
# $a2 = max number of iterations	
#
#	
# Returns
# None
#	
#
# Register Usage
# $s0 = rows
# $s1 = cols
# $s2 = row iterations
# $s3 = col iterations
# $s4 = max iterations	
########################################################################

	#Stack Adjustments
	addi	$sp, $sp, -4
	sw	$fp, 0($sp)
	add	$fp, $zero, $sp
	addi	$sp, $sp, -24
	sw	$ra, -4($fp)
	sw	$s0, -8($fp)
	sw	$s1, -12($fp)
	sw	$s2, -16($fp)
	sw	$s3, -20($fp)
	sw	$s4, -24($fp)
	
	#$s4 = max iterations
	add	$s4, $a2, $0
	
        #$s0 = rows
	add	$s0, $a0, $0	

        #$s1 = cols
        add 	$s1, $a1, $0

        #s2 = row iterations
        add 	$s2, $0, $0
row_loop:

        #s3 = col iterations
        add 	$s3, $0, $0

col_loop:

	#setup and call map_coords
        add 	$a0, $s2, $0
        add 	$a1, $s3, $0
        jal 	map_coords

	#setup and call calculate_escape
        la 	$a0, x_0
        s.d 	$f0, 0($a0)
        la 	$a0, y_0
        s.d 	$f2, 0($a0)
	add 	$a0, $s4 $0
        jal 	calculate_escape

	#if it escaped go to escaped
        beq 	$v0, 1 escaped

	#default color black loaded
	la      $a0, inSetColor
        lbu     $a0, 0($a0)
        add     $a1, $0, $0
        jal     setColor

	#default symbol 'M' loaded
        la      $a0, inSetSymbol
	add     $a1, $s2, $0
        add     $a2, $s3, $0
        jal     printString
	j	iter

escaped:
	#$t4 = calculate_escape iterations % paletteSize
        la 	$a0, paletteSize
        lw 	$a0, 0($a0)
        div 	$t4, $v1, $a0
        mfhi 	$t4

	# loads color at position $t4
	la      $a0, colors
        add     $a0, $a0, $t4
        lbu     $a0, 0($a0)
        add     $a1, $0, $0
        jal     setColor

	#loads symbol at position 2*$t4
        la 	$a0, symbols
	sll	$t5, $t4, 1
        add 	$a0, $a0, $t5
        add 	$a1, $s2, $0
        add 	$a2, $s3, $0
        jal 	printString

iter:   addi 	$s3, $s3, 1
        blt 	$s3, $s1, col_loop

        add 	$s2, $s2, 1
        blt 	$s2, $s0, row_loop

	#Stack Restore
	lw	$ra, -4($fp)
	lw	$s0, -8($fp)
	lw	$s1, -12($fp)
	lw	$s2, -16($fp)
	lw	$s3, -20($fp)
	lw	$s4, -24($fp)
	addi	$sp, $sp, 24
	lw	$fp, 0($sp)
	addi	$sp, $sp, 4

	jr 	$ra

