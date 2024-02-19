# Student-Project Matching

## Overview

Our initial goal is to create a web app that matches students to projects. Each student has rank-ordered preferences for one or more projects. Projects have a set capacity and have rank-ordered preferences.

### Algorithm in Pseudocode

Abraham, David J., Robert W. Irving, and David F. Manlove. “Two Algorithms for the Student-Project Allocation Problem.” Journal of Discrete Algorithms 5, no. 1 (March 1, 2007): 73–90. https://doi.org/10.1016/j.jda.2006.03.006.

SPA-student(7) (
assign each student to be free;
assign each project and lecturer to be totally unsubscribed; while (some student s; is free and s; has a non-empty list) 1
Pj = first project on s;'s list;
x = lecturer who offers pj;
/* s; applies to p; */
provisionally assign s; to pj:
/* and to lk */
if (p; is over-subscribed) 1|
S, = worst student assigned to pj;
/* according to C, *,
break provisional assignment between s, and pj:
else if (le is over-subscribed) f
Sp = worst student assigned to lk:
Pr = project assigned sy;
break provisional assignment between s, and pr;
if (p; is full) (
sr = worst student assigned to pj:
for (each successors, of s, on 6l) delete (st. P;):
* according to C*,
if (Ix is full) (
Sr = worst student assigned to i;
for (each successor s, of s, on (k) for (each project pu € Pan A,)
delete (5+- Pu):
return ((si-Pj) €S x P: s; is provisionally assigned to pj: