#----------------------------------------------------------------
#
# CMPUT 229 Student Submission License
# Version 1.0
# Copyright 2017 Kyle Fujishige
#
# Redistribution is forbidden in all circumstances. Use of this software
# without explicit authorization from the author is prohibited.
#
# This software was produced as a solution for an assignment in the course
# CMPUT 229 - Computer Organization and Architecture I at the University of
# Alberta, Canada. This solution is confidential and remains confidential 
# after it is submitted for grading.
#
# Copying any part of this solution without including this copyright notice
# is illegal.
#
# If any portion of this software is included in a solution submitted for
# grading at an educational institution, the submitter will be subject to
# the sanctions for plagiarism at that institution.
#
# If this software is found in any public website or public repository, the
# person finding it is kindly requested to immediately report, including 
# the URL or other repository locating information, to the following email
# address:
#
#          cmput229@ualberta.ca
#
#---------------------------------------------------------------
# Lab			4
# Due Date:             November 20, 2017
# Name:                 Kyle Fujishige
# Unix ID:              fujishig
# Lecture Section:      A1
# Instructor:           J Nelson Amaral
# Lab Section:          D07 (Tuesday 0200 - 0500)
# Teaching Assistant:   TBA
#---------------------------------------------------------------
#
#Program header:
#			minesweeper_KF.s	
#
#---------------------------------------------------------------
#kdata section:
#---------------------------------------------------------------
# This particular exception/interrupt handler only needs to use
# 3 variables. Thus we only need 3 words to save t0, t1, and t2.
#---------------------------------------------------------------
	
.kdata
save0:	.word 0
save1:	.word 0
save2:	.word 0
	
#---------------------------------------------------------------
#ktext section:
#---------------------------------------------------------------
# Due to the MIPS 32 convention, an interrupt or exception will
# automatically jump to 0x80000180, thus this needs to be included
# when creating your own exception handler. This exception handler
# actually gets called when there is either a keyboard interupt or	
# a timer interrupt. Depending on which one, the exception handler
# will redirect the flow of the program accordingly.	
#
#	
# Register Usage:
#
#	k0: holds the cause register at first, then acts as a temp
#	k1: always holds the at and is NEVER used beyond this.	
#	t0-t2: temporary variables for various instructions	
#
# Returns:
#	EPC will go to necessary spot in main function depending
#	on what kind of interrupt caused this (incrimenting $14
#	to its respective PC spot.)
#---------------------------------------------------------------
	
.ktext 	0x80000180
	mtc0	$0, $12			#clear status register
	.set 	noat			
	move 	$k1 $at			#set mode to no at so
	.set 	at			#we can store at.
	mfc0	$k0, $13		#k0 is cause register
	sw	$t0, save0
	sw	$t1, save1		#save the necessary registers
	sw	$s1, save2
	la	$t0, 0xffff0000
	lw	$t1, 0($t0)		#grab the keyboard status and
	sw	$0, 0($t0)		#clear the keyboard status.
	andi	$t1, $t1, 0x1		#check first bit of the keyboard
	li	$t2, 1			#status to see if this is a keyboard
	beq	$t1, $t2, keyInt	#interupt
	srl	$t0, $k0, 15		
	li	$t1, 1			#check cause registers 15th bit for
	beq	$t0, $t1, timeInt	#timer interrupt
	mfc0	$t0, $12	
	ori	$t0, $t0, 0x801		#if this is neither a keyboard or
	mtc0	$t0, $12		#timer, reset interrupts and 
	li	$t0, 0x3		#keyboard status, and jump
	la	$t1, 0xffff0000		#out of the handler.
	sw	$t0, 0($t1)
	j	doneInt
	
keyInt:
	la	$t0, 0xffff0004		#keyboard interrupt first checks
	lw	$t0, 0($t0)		#what kind of key was pressed
	li	$t1, -1			#it will branch to the respective
	ble	$s1, $t1, endThisThing	#areas depending on what was pressed.
        li      $t1, 53
        beq     $t0, $t1 Reveal		#reveal a tile
        li      $t1, 55
        beq     $t0, $t1, mark		#mark a tile
	
					#only checks the keys below this
endThisThing:				#point when player either wins
					#or loses.
        li      $t1, 54
        beq     $t0, $t1, right		#move cursor to the right
        li      $t1, 52
        beq     $t0, $t1, left		#move cursor to the left
        li      $t1, 56
        beq     $t0, $t1, up		#move cursor up
        li      $t1, 50
        beq     $t0, $t1, down		#move cursor down
        li      $t1, 113
        beq     $t0, $t1, quit		#quit
        li      $t1, 114
        beq     $t0, $t1, reset		#reset
        j       invalidKey		#invalid key handler

Reveal:	la	$t0, cursorRow		
	lw	$t0, 0($t0)
	la	$t1, cursorCol
	lw	$t1, 0($t1)
	la	$t2, gameCols
	lw	$t2, 0($t2)
	mul	$t0, $t0, $t2
	add	$t0, $t0, $t1
	la	$t1, state		#reveal first checks the state
	add	$t1, $t1, $t0		#of the current tile and goes
	lb	$t0, 0($t1)		#to invalid key if this tile
	li	$t2, 0x2		#can't be revealed.
	beq	$t2, $t0, invalidKey
	li	$t2, 0x1
	beq	$t2, $t0, invalidKey
	mfc0	$t0, $14		#ensures the PC goes to reveal
	addi	$t0, $t0, 12		#tile function.
	mtc0	$t0, $14
	j	doneInt
	

quit:	
	mfc0	$t0, $14		#PC will go to the done function
	addi	$t0, $t0, 20
	mtc0	$t0, $14
	j	doneInt

reset:
	mfc0	$t0, $14		#PC will go to the reset2 function
	addi	$t0, $t0, 16
	mtc0	$t0, $14
	j	doneInt
	
mark:	la	$t0, cursorRow
	lw	$t0, 0($t0)
	la	$t1, cursorCol
	lw	$t1, 0($t1)
	la	$t2, gameCols
	lw	$t2, 0($t2)
	mul	$t0, $t0, $t2
	add	$t0, $t0, $t1
	la	$t1, state		#mark checks to see if this tile
	add	$t1, $t1, $t0		#has already been revealed first.
	lb	$t0, 0($t1)
	li	$t2, 0x1
	beq	$t0, $t2, invalidKey
	li	$t2, 0x2		#it will mark or unmark depending
	beq	$t0, $t2, unmark	#on the tiles current state 
	sb	$t2, 0($t1)		#(2 = marked)
	j	KeySt
unmark:
	sb	$0, 0($t1)		#(0 = unmarked/unrevealed)
	j	KeySt
	
right:	la	$t0, cursorCol		#move cursor to the right.
	lw	$t1, 0($t0)
	addi	$t1, $t1, 1
	la	$t2, gameCols
	lw	$t2, 0($t2)
	la	$t0, newCursorCol
	bge	$t1, $t2, noRight	#won't go to the right if
	sw	$t1, 0($t0)		#it's 1 below the total game
	j	KeySt			#columns.
noRight:
	addi	$t2, $t2, -1		
	sw	$t2, 0($t0)
	j	KeySt


left:	la	$t0, cursorCol		#move cursor to the left.
	lw	$t1, 0($t0)
	addi	$t1, $t1, -1
	la	$t0, newCursorCol
	blt	$t1, $0, noLeft		#won't go to the left if
	sw	$t1, 0($t0)		#it's currently at the 0
	j	KeySt			#column.
noLeft:
	addi	$t1, $t1, 1
	sw	$t1, 0($t0)
	j	KeySt

up:	la	$t0, cursorRow		#move cursor up.
	lw	$t1, 0($t0)
	addi	$t1, $t1, -1
	la	$t0, newCursorRow
	blt	$t1, $0, noUp		#won't go up past the
	sw	$t1, 0($t0)		#0 row.
	j	KeySt
noUp:
	addi	$t1, $t1, 1
	sw	$t1, 0($t0)
	j	KeySt

down:	la	$t0, cursorRow		#move cursor down.
	lw	$t1, 0($t0)
	addi	$t1, $t1, 1
	la	$t2, gameRows
	lw	$t2, 0($t2)
	la	$t0, newCursorRow
	bge	$t1, $t2, noDown	#won't go past the game row size.
	sw	$t1, 0($t0)
	j	KeySt
noDown:
	addi	$t2, $t2, -1
	sw	$t2, 0($t0)
	j	KeySt

	
invalidKey:				#invalid key resets status
	mfc0    $t0, $12		#register and keyboard
	ori	$t0, $t0, 0x8801	#status.
	mtc0	$t0, $12
	la	$t0, 0xffff0000
	li	$t1, 0x3
	sw	$t1, 0($t0)
	j	doneInt
	
	
	
KeySt:	mfc0	$t0, $14		#will go to the PC spot that
	addi	$t0, $t0, 8		#updates the cursor when it's
	mtc0	$t0, $14		#moved.
	j	doneInt

	
timeInt:				#timer interrupt resets the
	mtc0	$0, $9			#$9 register and the $11
	li	$t0, 100		#register so that it will
	mtc0	$t0, $11		#throw a timer interrupt again
	mfc0	$t0, $14		#in 1 second.
	addi	$t0, $t0, 4
	mtc0	$t0, $14
	mfc0	$k0, $12
	ori	$k0, $k0, 0x8801	#reset the status register
	mtc0	$k0, $12
	j	doneInt
	
doneInt:
	mtc0 	$0, $13			# Clear Cause register
	lw	$t0, save0
	lw	$t1, save1		# Restore old values
	lw	$t2, save2
	
	.set 	noat
	move 	$at, $k1		# Restore $at
	.set 	at
	eret

#---------------------------------------------------------------
#data section:
#---------------------------------------------------------------
#state:		represents the status of each tile on the board.
#countDown:	holds the binary representation needed to print
#		the time to the bottom of the board.
#numTiles:	Represents the number of tiles left to be
#		to be revealed that aren't bombs.
#---------------------------------------------------------------
.data
state:
	.align 2
	.space 800
countDown:
	.word 0
numTiles:
	.word 0

#---------------------------------------------------------------
#main:
#---------------------------------------------------------------
# main function will first setup the time, keyboard status,
# and interrupts, and then go into an infinite loop. Once in
# the infinite loop, it will exit when an interrupt happens.
# under the infinite loop there are places it can jump to depending
# on what the exception handler determined is the appropriate
# action.

# register usage:
#	s0: holds the value of the current time.
#	s1: status of game to determine if it's first move
#	    or player has won/lost.
#	t0-t4: temporary registers used for various instructions
#	a0-a3: inputs for various function calls.

# returns:
#	v0: 1 to reset the game, 0 to end the game.
#---------------------------------------------------------------
	
.text
main:
	addi	$sp, $sp, -4
	sw	$fp, 0($sp)
	move	$fp, $sp
	addi	$sp, $sp, -16
	sw	$ra, -4($fp)
	sw	$s0, -8($fp)
	sw	$s1, -12($fp)
	sw	$s2, -16($fp)
	
	la	$s0, totalBombs
	lw	$s0, 0($s0)
	la	$t0, numTiles
	lw	$t1, 0($t0)
	sub	$t1, $t1, $s0
	beq	$t1, $0, max_time	#can't divide by 0.
	sw	$t1, 0($t0)			
	li	$s1, 888		#time calculation:
	mul	$t2, $s0, $s1		#time = totalBombs*888/tiles
	div	$s0, $t2, $t1
	li	$t0, 999
	bge	$s0, $t0, max_time	#max time = 999
	li	$t0, 5
	ble	$s0, $t0, min_time	#min time = 5
	j	done_time1
max_time:
	li	$s0, 999
	j	done_time1

min_time:
	li	$s0, 5
	
done_time1:
	li	$s1, 0			#fun fact: change s1 to 1 and
					#you can play with no timer.

	li	$t0, -1			#ensures no timer interrupt
	mtc0	$t0, $11		#will happen.
done_time:
        mfc0    $t0, $12
	ori	$t0, $t0, 0x8801
	mtc0	$t0, $12
	la	$t0, 0xffff0000
	li	$t1, 0x3
	sw	$t1, 0($t0)
	
	
infinite:
	j	infinite		#infinite loop
	
	j	setTimer		#various jumps depending on
	j	cursorMove		#interrupt that happened.
	j	revealTile
	j	reset2
	j	done
	
revealTile:
	la      $t0, cursorRow
        lw      $a0, 0($t0)
        la      $t1, cursorCol
        lw      $a1, 0($t1)
	jal	getTile			#gets the tile state
	li	$t1, 1			#makes the tile state
	sb	$t1, 0($v1)		#revealed. (1 = revealed)
	la      $t0, cursorRow
        lw      $a0, 0($t0)
        la      $t1, cursorCol			
        lw      $a1, 0($t1)
	jal	getTile			#reveals tile.
	la      $t0, bomb
        beq     $t0, $v0, lose		#loses if it's a bomb.
	bne	$s1, $0, notFirst		
	li	$t0, 95			#if this is first reveal,
	mtc0	$t0, $9			#sets up timer interrupt.
	li	$t0, 100
	mtc0	$t0, $11
	addi	$s1, $s1, 1
notFirst:
	la	$t0, has0		#if the tile is a 0
	bne	$t0, $v0, noRecursion	#begin recursive flood fill.
	
	sb	$0, 0($v1)
	la	$t0, cursorRow
	lw	$a0, 0($t0)
	la	$t1, cursorCol
	lw	$a1, 0($t1)
	la	$t0, gameRows
	lw	$a2, 0($t0)
	la	$t1, gameCols
	lw	$a3, 0($t1)		#setup and call the
	jal	recursiveReveal		#recursive flood fill.
	j	noReveal
	
	
noRecursion:
	la	$t0, numTiles
	lw	$t1, 0($t0)
	addi	$t1, $t1, -1
	sw	$t1, 0($t0)
	la      $t0, cursorRow		#print the tile and update
        lw      $a0, 0($t0)		#number of tiles if this is
        la      $t1, cursorCol		#a single tile reveal.
        lw      $a1, 0($t1)
	jal	printTile

noReveal:
	la      $t0, numTiles		#goes back to the interrupt
        lw      $t1, 0($t0)		#setup, and checks to see
	ble	$t1, $0, win		#if player has won. (Tiles
	j	done_time		#has reached 0)

	
cursorMove:
	jal	updateCursor		#cursor has moved
	j	done_time

	
setTimer:
	addi	$s0, $s0, -1
	li	$t0, 48
	li	$t1, 10
	div	$s0, $t1
	mfhi	$t1 
	li	$t3, 100
	div	$s0, $t3
	mflo	$t3
	mfhi	$t2
	li	$t4, 10
	div	$t2, $t4
	mflo	$t2
	add	$t1, $t1, $t0
	add	$t2, $t2, $t0
	add	$t3, $t3, $t0
	la	$t4, countDown		#setup the binary ascii
	sb	$t1, 2($t4)		#representation of the
	sb	$t2, 1($t4)		#current timers time
	sb	$t3, 0($t4)		#so it can print it.
	sb	$0, 3($t4)
	j	printTime

printTime:
	la	$a0, countDown		#print the time to the
	la	$a1, gameRows		#bottom row+1.
	lw	$a1, 0($a1)
	addi	$a1, $a1, 1
	move	$a2, $0
	jal	printString
	beq	$s0, $0, lose
	j	done_time

lose:	jal	updateCursor		#lose prints the losing
	la	$a0, gameLost		#sequence to the bottom
	la	$a1, gameRows		#of the screen and sets
	lw	$a1, 0($a1)		#up s1 so it will ensure
	addi	$a1, $a1, 1		#only movement commands
	move	$a2, $0			#can be made.
	jal	printString
	li	$t0, 0x8801
	mtc0	$t0, $12
	la	$t0, 0xffff0000
	li	$t1, 0x3
	sw	$t1, 0($t0)
	addi	$s1, $0, -1
	mtc0	$s1, $11		#ensures no timer interrupt
	j	infinite		#can happen.

win:	jal	updateCursor		#win prints the winning
	la	$a0, gameWon		#sequence to the bottom
	la	$a1, gameRows		#of the screen and sets
	lw	$a1, 0($a1)		#up s1 so it will ensure
	addi	$a1, $a1, 1		#only movement commands
	move	$a2, $0			#can be made.
	jal	printString
	li	$t0, 0x8801
	mtc0	$t0, $12
	la	$t0, 0xffff0000
	li	$t1, 0x3
	sw	$t1, 0($t0)
	addi	$s1, $0, -1
	mtc0	$s1, $11		#ensures no timer interrupt
	j	infinite		#can happen.
	


done:	move	$v0, $0			#v0 = 0, quits the program.
	j	exit
reset2:	li	$v0, 1
	la	$t0, numTiles		#v0 = 1, resets the program.
	sw	$0, 0($t0)		#resets both numTiles and
	la	$t0, countDown		#countDown.
	sw	$0, 0($t0)
exit:	mtc0	$0, $12
	la	$t0, 0xffff0000		#disables interrupts and
	sw	$0, 0($t0)		#keyboard interrupts.
	lw	$ra, -4($fp)		#exits main.
	lw	$s0, -8($fp)
	lw	$s1, -12($fp)
	lw	$s2, -16($fp)
	addi	$sp, $sp, 16
	lw	$fp, 0($sp)
	addi	$sp, $sp, 4
	jr	$ra


#---------------------------------------------------------------
#recursiveReveal:
#---------------------------------------------------------------
#recursiveReveal is first called if the player has revealed a 0 tile.
#This function uses a clockwise 8-way flood fill algorithm to fill
#any neighboring tiles. The base case is if the tile is not a 0, or
#extends past the frame of the board.	

#inputs:
#	a0: current row
#	a1: current col
#	a2: total game rows	
#	a3: total game columns

#register usage:
#	s0: current row
#	s1: current col
#	s2: game rows
#	s3: game cols
#	s4: state address
#	s5: incrimenter to the state
#	a0: new row for next recursive call
#	a1: new col for next recursive call
#	a2: total game rows
#	a3: total game columns
#	t0-t2: temporary registers used for various instructions.

#returns:
	#nothing, but continuously updates the board and numTiles
	#as it goes through each recursive cycle.
#---------------------------------------------------------------
	
recursiveReveal:
	addi	$sp, $sp, -4
	sw	$fp, 0($sp)
	move	$fp, $sp
	addi	$sp, $sp, -28
	sw	$ra, -4($fp)
	sw	$s0, -8($fp)
	sw	$s1, -12($fp)
	sw	$s2, -16($fp)
	sw	$s3, -20($fp)
	sw	$s4, -24($fp)
	sw	$s5, -28($fp)
	
	move	$s0, $a0		#s0 = current row
	move	$s1, $a1		#s1 = current col
	move	$s2, $a2		#s2 = game rows
	move	$s3, $a3		#s3 = game cols
	la	$s4, state

	#li	$v0, 5
	#syscall

	li	$t0, -1
	beq	$s0, $t0, endRecursion	#checking outer limits of the board
	beq	$s1, $t0, endRecursion
	beq	$s0, $s2, endRecursion
	beq	$s1, $s3, endRecursion

	mul	$s5, $s0, $s3
	add	$s5, $s5, $s1
	add	$t0, $s4, $s5
	lb	$t1, 0($t0)
	li	$t2, 2
	beq	$t1, $t2, endRecursion	#check if this tile is marked
	li	$t2, 1
	beq	$t1, $t2, endRecursion	#check if this tile has already been
					#revealed
	
	sb	$t2, 0($t0)		#change the tiles state
	la	$t0, numTiles		#reduce the number of tiles by 1.
	lw	$t1, 0($t0)
	addi	$t1, $t1, -1
	sw	$t1, 0($t0)
	
	move	$a0, $s0
	move	$a1, $s1
	jal	printTile		#print the tile
	move	$a0, $s0
	move	$a1, $s1
	jal	getTile
	la	$t0, has0		#if this tile is not a 0,
	bne	$t0, $v0, endRecursion	#end recursion
	

	addi	$a0, $s0, -1 		#check top middle
	move	$a1, $s1
	move	$a2, $s2
	move	$a3, $s3
	jal	recursiveReveal

	addi	$a0, $s0, -1		#check top right
	addi	$a1, $s1, 1
	move	$a2, $s2
	move	$a3, $s3
	jal	recursiveReveal

	move	$a0, $s0		#check middle right
	addi	$a1, $s1, 1
	move	$a2, $s2
	move	$a3, $s3
	jal	recursiveReveal

	addi	$a0, $s0, 1		#check bottom right
	addi	$a1, $s1, 1
	move	$a2, $s2
	move	$a3, $s3
	jal	recursiveReveal

	addi	$a0, $s0, 1		#check bottom middle
	move	$a1, $s1
	move	$a2, $s2
	move	$a3, $s3
	jal	recursiveReveal

	addi	$a0, $s0, 1		#check bottom left
	addi	$a1, $s1, -1
	move	$a2, $s2
	move	$a3, $s3
	jal	recursiveReveal

	move	$a0, $s0		#check middle left	
	addi	$a1, $s1, -1
	move	$a2, $s2
	move	$a3, $s3
	jal	recursiveReveal

	addi	$a0, $s0, -1		#check top left
	addi	$a1, $s1, -1
	move	$a2, $s2
	move	$a3, $s3
	jal	recursiveReveal
	
endRecursion:
	
        lw      $ra, -4($fp)
        lw      $s0, -8($fp)
        lw      $s1, -12($fp)
        lw      $s2, -16($fp)
        lw      $s3, -20($fp)
        lw      $s4, -24($fp)
        lw      $s5, -28($fp)
        addi    $sp, $sp, 28
        lw      $fp, 0($sp)
        addi    $sp, $sp, 4
        jr      $ra
	
#---------------------------------------------------------------
# getTile:
#---------------------------------------------------------------
# getTile will figure out what the current tiles state is,
# and then return the tiles contents depending on its state.
# as well as the address of the current tiles state.
#
# inputs:
# 	a0: row of tile
#	a1: col of tile	
#
# register usage:
#	t0-t2: temporary registers used for various instructions	
#
# returns:
#	v0: address of tiles string representation
#	v1: address of the tiles state	
#---------------------------------------------------------------
getTile:
	la	$v1, state
	la	$t1, gameCols
	lw	$t1, 0($t1)
	mul	$t1, $a0, $t1
	add	$t1, $t1, $a1
	add	$v1, $v1, $t1		#v1: address of the state
	lb	$t2, 0($v1)		#of the tile.
	la	$t0, gameBoard
	add	$t0, $t0, $t1
	lbu	$t0, 0($t0)
	beq	$t2, $0, hidTile	#checks the tiles contents:
	li	$t1, 2
	beq	$t2, $t1, markedTile
	
	beq	$t0, $0, zero
	li	$t1, 1
 	beq	$t0, $t1, one
	li	$t1, 2
 	beq	$t0, $t1, two
	li	$t1, 3
 	beq	$t0, $t1, three
	li	$t1, 4
	beq	$t0, $t1, four
	li	$t1, 5
 	beq	$t0, $t1, five
	li	$t1, 6
 	beq	$t0, $t1, six
	li	$t1, 7
	beq	$t0, $t1, seven
	li	$t1, 8
 	beq	$t0, $t1, eight
					#returns the string
	la	$v0, bomb		#representation in v0
	jr	$ra
hidTile:	
	la	$v0, tile
	jr	$ra
markedTile:
	la	$v0, marked
	jr	$ra
zero:	la	$v0, has0
	jr	$ra
one:	la	$v0, has1
	jr	$ra
two:	la	$v0, has2
	jr	$ra
three:	la	$v0, has3
	jr	$ra
four:	la	$v0, has4
	jr	$ra
five:	la	$v0, has5
	jr	$ra
six:	la	$v0, has6
	jr	$ra
seven:	la	$v0, has7
	jr	$ra
eight:	la	$v0, has8
	jr	$ra


#---------------------------------------------------------------
#prepareBoard:
#---------------------------------------------------------------
#prepareBoard will setup the gameBoard to have each of the tiles
#that have any neighboring bombs to have the numbers corresponding
#to the number of neighboring bombs. It also sets up the state 	
#of each tile to be hidden.
#
#inputs: None
#
#register usage:
#	s0: current row
#	s1: current col
#	s2: current address spot in gameBoard	
#	s3: row of number update
#	s4: col of number update
#	s5: gameBoard address number update 
#	t0-t2: temporary registers used for various instructions
#---------------------------------------------------------------
prepareBoard:
	addi	$sp, $sp, -4
	sw	$fp, 0($sp)
	move	$fp, $sp
	addi	$sp, $sp, -28
	sw	$ra, -4($fp)
	sw	$s0, -8($fp)
	sw	$s1, -12($fp)
	sw	$s2, -16($fp)
	sw	$s3, -20($fp)
	sw	$s4, -24($fp)
	sw	$s5, -28($fp)

	li	$s0, 0
while1:	la	$t0, gameRows
	lw	$t0, 0($t0)		#nested while loops to check every
	bge	$s0, $t0, endLoop	#row and column.
	li	$s1, 0
while2:	la	$t0, gameCols
	lw	$t0, 0($t0)
	bge	$s1, $t0, endCol

	la	$s2, state
	la	$s3, gameCols
	lw	$s3, 0($s3)
	mul	$s4, $s0, $s3
	add	$s4, $s4, $s1		#makes each tiles state 0
	add	$s2, $s2, $s4		#(0 = unrevealed)
	sb	$0, 0($s2)

	
	la	$s2, numTiles
	lw	$s3, 0($s2)
	addi	$s3, $s3, 1		#counts the number of tiles.
	sw	$s3, 0($s2)

	la	$s2, gameBoard
	mul	$t0, $s0, $t0
	add	$t0, $t0, $s1		#calculates current spot in
	add	$s2, $s2, $t0		#gameBoard.

	la	$t2, bomb
	lbu	$t0, 0($t2)		#checks if current spot is a bomb.
	lbu	$t1, 0($s2)
	bne	$t0, $t1, nobom
	
	
	move	$s3, $s0		#if it's a bomb, we do another loop.
	move	$s4, $s1		#This loop checks all 8 spots around
	move	$s5, $s2		#the bomb.
	
	la	$t0, gameCols
	lw	$t0, 0($t0)
	beq	$s3, $0, row_edge
	addi	$s3, $s3, -1
	sub	$s5, $s5, $t0		#sets up nested loop, checks to see
row_edge:				#if bomb is on the edge.
	beq	$s4, $0, col_edge
	addi	$s4, $s4, -1
	addi	$s5, $s5, -1
col_edge:
	lbu	$t0, 0($s5)
	la	$t1, bomb
	lbu	$t1, 0($t1)
	beq	$t1, $t0, continue1
	
	addi	$t0, $t0, 1		#incriments surrounding blank tiles
	sb	$t0, 0($s5)
	
continue1:
	addi	$s4, $s4, 1
	addi	$s5, $s5, 1
	addi	$t0, $s1, 2
	li	$t1, -2
	bge	$s4, $t0, continue2
	la	$t0, gameCols
	lw	$t0, 0($t0)
	li	$t1, -1
	bge	$s4, $t0, continue2
	j	col_edge

continue2:	
	addi	$s3, $s3, 1
	add	$s5, $s5, $t1
	addi	$t0, $s0, 2
	bge	$s3, $t0, nobom
	la	$t0, gameRows
	lw	$t0, 0($t0)
	bge	$s3, $t0, nobom
	la	$t0, gameCols
	lw	$t0, 0($t0)
	add	$s5, $s5, $t0
	move	$s4, $s1
	j	row_edge
	
	
	
nobom:	addi	$s1, $s1, 1
	j	while2
endCol:	addi	$s0, $s0, 1
	j	while1
endLoop:
	lw	$ra, -4($fp)
	lw	$s0, -8($fp)
	lw	$s1, -12($fp)
	lw	$s2, -16($fp)
	lw	$s3, -20($fp)
	lw	$s4, -24($fp)
	lw	$s5, -28($fp)
	addi	$sp, $sp, 28
	lw	$fp, 0($sp)
	addi	$sp, $sp, 4
	jr	$ra

#---------------------------------------------------------------
#hasBomb:	
#---------------------------------------------------------------
#checks current tile to see if it has a bomb. 
#
#inputs:
#	a0: current row
#	a1: current col
#register usage:
#	t0-t2: temporary registers used for various instructions
#	
#returns:
#	v0: 1 = has a bomb. 0 = not a bomb.	
#---------------------------------------------------------------
hasBomb:
	la	$t0, bomb
	lbu	$t0, 0($t0)
	la	$t1, gameBoard
	la	$t2, gameCols
	lw	$t2, 0($t2)
	mul	$t2, $a0, $t2
	add	$t2, $t2, $a1
	add	$t1, $t1, $t2
	lbu	$t1, 0($t1)
	li	$v0, 0
	bne	$t0, $t1, donehas
	li	$v0, 1
donehas:
	jr	$ra

#---------------------------------------------------------------
#setBomb:
#---------------------------------------------------------------
#sets a bomb at current tile. 
#
#inputs:
#	a0: current row
#	a1: current col
#register usage:
#	t0-t2: temporary registers used for various instructions
#	
#returns:
#	nothing
#---------------------------------------------------------------
setBomb:
	la	$t0, bomb
	lbu	$t0, 0($t0)
	la	$t1, gameBoard
	la	$t2, gameCols
	lw	$t2, 0($t2)
	mul	$t2, $t2, $a0
	#addi	$t2, $t2, 1
	add	$t2, $t2, $a1
	add	$t1, $t1, $t2
	
	sb	$t0, 0($t1)
	jr	$ra

#---------------------------------------------------------------
#printTile:
#---------------------------------------------------------------
#prints the current tile to the screen.
#
#inputs:
#	a0: current row
#	a1: current col
#register usage:
#	s0: holds current row during function call
#	s1: holds current col during function call
#	a0: address of current tiles string representation
#	a1: current row for function call printString
#	a2: current col	for functionc all printString
#	
#returns:
#	nothing	
#---------------------------------------------------------------
printTile:
	addi	$sp, $sp, -12
	sw	$ra, 0($sp)
	sw	$s0, 4($sp)
	sw	$s1, 8($sp)
	move	$s0, $a0
	move	$s1, $a1
	jal	getTile
	move	$a1, $s0
	move	$a2, $s1
	move	$a0, $v0
	jal	printString
donePrint:
	lw	$ra, 0($sp)
	lw	$s0, 4($sp)
	lw	$s1, 8($sp)
	addi	$sp, $sp, 12
	jr	$ra
