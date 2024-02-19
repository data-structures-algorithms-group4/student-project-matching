# Student-Project Matching

## Overview

Our initial goal is to create a web app that matches students to projects. Each student has rank-ordered preferences for one or more projects. Projects have a set capacity and have rank-ordered preferences.

### Algorithm in Pseudocode

Abraham, David J., Robert W. Irving, and David F. Manlove. “Two Algorithms for the Student-Project Allocation Problem.” Journal of Discrete Algorithms 5, no. 1 (March 1, 2007): 73–90. https://doi.org/10.1016/j.jda.2006.03.006.

assign each student to be free;

assign each project and lecturer to be totally unsubscribed;

while (some student s; is free and s; has a non-empty list) {

$P_j$ = first project on $s_i$'s list;

$l_k$ = lecturer who offers $p_j$; /* $s_i$ applies to $p_j$ */

provisionally assign $s_i$ to $p_j$: /* and to $l_k$ */

if ($p_j$ is over-subscribed) {

$s_r$ = worst student assigned to $p_j$; /* according to $L^j_k$ *,
break provisional assignment between $s_r$ and $p_j$; }

else if ($l_k$ is over-subscribed) {

$s_r$ = worst student assigned to $l_k$:

$p_t$ = project assigned $s_r$;

break provisional assignment between $s_r$ and $p_t$;
}
if ($p_j$ is full) {

$s_r$ = worst student assigned to $p_j$: * according to $L^j_k$*

for (each successor $s_t$ of $s_r$ on $L^j_k$ delete ($s_t$, $p_j$);
}
if ($l_k$ is full) {

$s_r$ = worst student assigned to $l_k$;

for (each successor $s_t$ of $s_r$ on $L_k$)

for (each project $p_u$ € $P_k$ $\union$ $A_t$)

delete ($s_t$, $p_u$);

}

}

}

return {($s_i$, $p_j$) in $S$ x $P$: $s_i$ is assigned to $p_j$};