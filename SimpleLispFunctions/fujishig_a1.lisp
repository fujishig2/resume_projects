; Cmput 325 Winter 2019 Assignment 1
; fujishig 1560138 Kyle Fujishige

;QUESTION 1 issorted
;Checks to see if a list given is in sorted order. True (T) will
;be returned if the list is in sorted order, and False (nil) will 
;be returned if the list isn't in sorted order.
;
;In order to do this we must go through the list in an iterative
;fashion. Thus, we will simply just recursively run a whole series
;of cat and cdr to remove the first number and compare it with the 
;previous number. If the list is empty, or has a single element
;then T is returned.
;
;Example
;   (issorted '()) => T
;   (issorted '(1)) => T
;   (issorted '(1 2 3)) => T
;   (issorted '(1 3 2)) => nil

(defun issorted (L)
  (if (or (null L) (null (cdr L)))
    T
    (if (>= (car L) (cadr L))
      nil
      (issorted (cdr L))
    )
  )  
)


;QUESTION 2 numbers
;When given a non-negative integer, this function will produce 
;a list of integers from 1 up to that integer. This means that
;we will have to recursively construct a list using the built in
;function list.
;
;Example
;   (numbers 0) => nil
;   (numbers 1) => '(1)
;   (numbers 5) => '(1 2 3 4 5)

(defun numbers (N)
  (cond ((= N 0) nil)
	((= N 1) (list 1))
	(T (append (numbers (- N 1)) (list N)))
  )
)


;QUESTION 3 palindrome
;When given an array of atoms, this function will be able to tell
;if the given array is a palindrome. This means that whether you
;read the array from left to right, or right to left, the values
;will all be the same and appear in the same order.
;
;This implementation of checking for a palindrome will use a
;helper function taken from the list-functions.lisp file
;myreverse. This function takes a list and reverses it.
;By doing this, we simply just check to see if the reverse is
;equal to the original list.
;
;Example
;   (palindrome '(a b c b a)) => T
;   (palindrome '(a b c b)) => nil
;   (palindrome '(a) => T
;   (palindrome nil => T
;

(defun myreverse (L)
  (if (null L)
    L
    (append (myreverse (cdr L))
	    (cons (car L) nil))
  )
)

(defun palindrome (L)
  (equal (myreverse L) L)
)


;QUESTION 4 replace1
;replace1 takes in 3 arguments. The arguments are 2 atoms and a
;list. This algorithm will search through a given list looking for
;atoms. If the atom matches the first argument, we replace the
;atom with the second atom given. Eventually the list will have
;all atoms that were once equal to the first atom replaced by
;the second atom. This does not work for nested lists.
;
;Example
;   (replace1 'a 'b '(a b a b a)) => '(b b b b b)
;   (replace1 'a 'b '(a b a (b a))) => '(b b b (b a))

(defun replace1 (A1 A2 L)
  (if (null L)
    nil
    (if (equal (car L) A1)
      (cons A2 (replace1 A1 A2 (cdr L)))
      (cons (car L) (replace1 A1 A2 (cdr L)))
    )
  )
)


;QUESTION 4 replace2
;replace2 takes in 3 arguments. The arguments are 2 atoms and a
;list. This algorithm will search through a given list looking for
;atoms. If the atom matches the first argument, we replace the
;atom with the second atom given. Eventually the list will have
;all atoms that were once equal to the first atom replaced by
;the second atom. This function will work on nested lists.
;
;Example
;   (replace1 'a 'b '(a b a b a)) => '(b b b b b)
;   (replace1 'a 'b '(a b a (b a))) => '(b b b (b b))

(defun replace2 (A1 A2 L)
  (if (null L)
    nil
    (if (atom (car L))
      (if (equal (car L) A1)
	(cons A2 (replace2 A1 A2 (cdr L)))
	(cons (car L) (replace2 A1 A2 (cdr L)))
      )
      (cons (replace2 A1 A2 (car L)) (replace2 A1 A2 (cdr L)))
    )
  )
)


;QUESTION 5 common
;When given 2 lists where no atom appears more than once in each
;list, this function will count how many atoms are contained in
;both of the lists. This means that this is a function which 
;counts the number of same atoms between the 2 lists.
;
;I also created a helper function mysearch to help with this task.
;mysearch simply is given an atom and a list, and searches for the
;atom within the given list. If it finds it, it returns True. If it
;can't find the atom, then there aren't any duplicates and mysearch
;returns nil.
;
;Example
;   (common '(1 2 3) '(3 2 1)) => 3
;   (common '(1 2 3 4) '(1 5 3 2)) => 3
;   (common '(a b c d) '(e f b g d)) => 2

(defun mysearch (A L)
  (if (null L)
    nil
    (if (eq (car L) A)
      T
      (mysearch A (cdr L))
    )
  )
)

(defun common (L1 L2)
  (if (null L1)
    0
    (if (mysearch (car L1) L2)
      (+ 1 (common (cdr L1) L2))
      (common (cdr L1) L2)
    )
  )
)


;QUESTION 6 setcover
;This is a function that will utilize the greedy algorithm to solve
;the set cover problem. Thus, the inputs will be a number N which is
;a list of numbers from 1 up to the number N. We will also be given
;a set of sets (S), where the algorithm will look for the minimum
;number of sets within S that cover the list of numbers from 1 to N.
;
;In this case, there were many helper functions being used. Each 
;helper function will be commented to explain what they do.
;
;
;Example 
;   ((let
;       ((S '((1 2 3) (2 4) (3 4) (2 5) (4 5))))
;       (setcover 5 S) => ((1 2 3) (4 5))
;   )
;   (let
;       ((S '((1 2) (2 3) (3 4) (4 5) (5 1))))
;       (setcover 5 S) => ((1 2) (3 4) (4 5))
;   )
;
;
;removelist takes a list L and removes all common elements between
;it and X. This means it will use the mysearch function in Q5 to find
;if there are common elements between X and L.
;
;Example
;   (removelist '(1 2 3 4 5) '(1 2)) => '(3 4 5)
;   (removelist '(1 2 3 4) '(1 4)) => '(2 3)

(defun removelist (L X)
  (if (null L)
    nil
    (if (mysearch (car L) X)
      (removelist (cdr L) X)
      (cons (car L) (removelist (cdr L) X))
    )
  )
)

;countsets takes the main set L, and finds the subset in S which
;has the most common elements. It returns the number which represents
;the largest number of common elements. This function uses the 
;common function from Q5 to get the number of common elements.


;Example
;   (countsets '(1 2 3 4 5) '(1 2) (1 2 3) (1)) => 3
;   (countsets '(1 2 3 4) '(1 4) (5 4) (1 2)) => 2

(defun countsets (L S)
  (if (null S)
    0
    (if (>= (common L (car S)) (countsets L (cdr S)))
      (common L (car S))
      (countsets L (cdr S))
    )
  )
)

;findset finds the set in S where the number of common elements
;is equal to the number N. This means that findset will return
;the set in S with the most common elements in L, provided that
;N is the value of the set with the largest number of common
;elements. This function uses the common function from Q5.
;
;Example
;   (findset 1 '(1 2 3 4 5) '((1 5) (3) (1 2 4))) => (3)
;   (findset 2 '(1 2 3 4 5) '((1 5) (3) (1 2 4))) => (1 5)
;   (findset 3 '(1 2 3 4 5) '((1 2) (3) (1 2 4))) => (1 2 4)

(defun findset (N L S)
  (if (null S)
    nil
    (if (= N (common (car S) L))
      (car S)
      (findset N L (cdr S))
    )
  )
)

;greedycover is used to construct a set of sets where it uses
;the greedy algorithm to find the minimum number of sets which
;covers the set in the given list L. This is accomplished 
;by combining all the helper functions.
;
;Example 
;   ((let
;       ((S '((1 2 3) (2 4) (3 4) (2 5) (4 5))))
;       (greedycover 5 S) => ((1 2 3) (4 5))
;   )
;   (let
;       ((S '((1 2) (2 3) (3 4) (4 5) (5 1))))
;       (greedycover 5 S) => ((1 2) (3 4) (4 5))
;   )

(defun greedycover (L S)
  (if (null L)
    nil
    (let ((X (findset (countsets L S) L S)))
      (cons X (greedycover (removelist L X) S))
    )
  )
)

(defun setcover (N S)
  (greedycover (numbers N) S)
)





