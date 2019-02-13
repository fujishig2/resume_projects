; Cmput 325 Winter 2019 Assignment 1
; Public test cases
; Martin Mueller

; How to use:
; First, load your assignment solution into SBCL
; Second, load this file.
; Third, fix the bugs and run this file again
; You can also copy+paste individual tests from here into SBCL

(defun test-case (ID Test Result)
    (if (equal Test Result)
        (format t "Test ~S OK~%" ID)
        (format t "FAIL: Test ~S expected ~S got ~S~%" ID Result Test)
    )
)

(test-case 1.1 (issorted '()) T)

(test-case 1.2 (issorted '(5)) T)

(test-case 1.3 (issorted '(5 9 12)) T)

(test-case 1.4 (issorted '(5 4)) nil)

(test-case 1.5 (issorted '(1 2 3 4 5)) T)

(test-case 1.6 (issorted '(1 2 3 4 5 5)) nil)


(test-case 2.1 (numbers 0) NIL)

(test-case 2.2 (numbers 1) '(1))

(test-case 2.3 (numbers 5) '(1 2 3 4 5))

(test-case 2.4 (numbers 100) '(
 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29
 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55
 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100))


(test-case 3.1 (palindrome '(a b c b a)) T)

(test-case 3.2 (palindrome '(a b c c b a)) T)

(test-case 3.3 (palindrome '(a b c a b)) nil)

(test-case 3.4 (palindrome nil) T)

(test-case 3.5 (palindrome '(a s i p e e s i r i s e e p i s a)) T)

(test-case 3.6 (palindrome '(i n g i r u m i m u s n o c t e e t c o n s u m i m u r i g n i)) T)


(test-case 4.1 (replace1 'a 'b '(a a b c a d)) '(b b b c b d))

(test-case 4.2 (replace1 'a 'b '(a (a))) '(b (a)))

(test-case 4.3 (replace1 'apple 'orange '(apple (apple apple orange) apple (apple (apple orange) orange))) '(orange (apple apple orange) orange (apple (apple orange) orange)))

(test-case 4.4 (replace2 'a 'b '(a a b c a d)) '(b b b c b d))

(test-case 4.5 (replace2 'a 'b '(a (a))) '(b (b)))

(test-case 4.6 (replace2 'apple 'orange '(apple (apple apple orange) apple (apple (apple orange) orange))) '(orange (orange orange orange) orange (orange (orange orange) orange)))

(test-case 5.1 (common nil nil) 0)
(test-case 5.2 (common '(a b c) nil) 0)
(test-case 5.3 (common '(a b c) '(a b c)) 3)
(test-case 5.4 (common '(a b c) '(c b a)) 3)
(test-case 5.5 (common '(a b c d) '(e f b g d)) 2)
(test-case 5.6 (common '(1 2 3 4 5 6) '(0 23 5 17)) 1)

; Question 6 easy test cases:

(test-case '6.easy.1
    (setcover 0 nil)
    nil
)

(test-case '6.easy.2
    (setcover 1 '((1)))
    '((1))
)

(test-case '6.easy.3
    (let
        ((S '((1 2 3 4 5))))
        (setcover 5 S)
    )
    '((1 2 3 4 5))
)

(test-case '6.easy.4
    (setcover 2 '((1) (2) (1 2)))
    '((1 2))
)

(test-case '6.easy.5
    (let
        ((S '((1) (2) (3) (4) (5))))
        (setcover 5 S)
    )
    '((1) (2) (3) (4) (5))
)

; Question 6 other test cases:

; The example from the assignment spec
(test-case '6.other.1
    (let
        ((S '((1 2 3) (2 4) (3 4) (2 5) (4 5))))
        (setcover 5 S)
    )
    '((1 2 3) (4 5))
)

; This case tests the tie-breaking by leftmost first
(test-case '6.other.2
    (let
        ((S '((1 2) (2 3) (3 4) (4 5) (5 1))))
        (setcover 5 S)
    )
    '((1 2) (3 4) (4 5))
)

; The next three cases are the example from the wikipedia page.
; In case 4 and 5, greedy is not optimal
(test-case '6.other.3
    (let
        ((S '((1 2) (3 4 5 6) (1 3 5) (2 4 6))))
        (setcover 6 S)
    )
    '((3 4 5 6) (1 2))
)

; Here, greedy needs 3 sets, but 2 would be optimal
(test-case '6.other.4
    (let
        ((S '((1 2) (3 4 5 6) (7 8 9 10 11 12 13 14) 
              (1 3 5 7 9 11 13) (2 4 6 8 10 12 14))))
        (setcover 14 S)
    )
    '((7 8 9 10 11 12 13 14) (3 4 5 6) (1 2))
)

; Here, greedy needs 4 sets, but 2 would be optimal
(test-case '6.other.5
    (let
        ((S '((1 2) (3 4 5 6) (7 8 9 10 11 12 13 14) 
              (15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30)
              (1 3 5 7 9 11 13 15 17 19 21 23 25 27 29) 
              (2 4 6 8 10 12 14 16 18 20 22 24 26 28 30))))
        (setcover 30 S)
    )
    '((15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30) (7 8 9 10 11 12 13 14) (3 4 5 6) (1 2))
)


