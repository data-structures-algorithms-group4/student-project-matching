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


### ChatGPT (selected) suggestions for algorithm enhancement:

1. **Incorporating Lecturer Preferences:** If projects are associated with lecturers who have their preferences for students, incorporating these preferences into the matching process could create a more balanced and mutually satisfactory matching outcome.
2. **Handling Ties in Preferences:** Implementing a more sophisticated method for handling ties in preferences (where a project or student is indifferent between multiple options) could improve match stability and satisfaction.
3. **Optimizing for Global Happiness:** Introducing a metric for overall satisfaction or "global happiness" of all participants and optimizing the algorithm to maximize this metric could lead to more universally satisfactory outcomes.
4. **Dynamic Capacity Management:** Allowing for dynamic adjustment of project capacities based on demand and preferences could make the matching process more flexible and capable of accommodating more students with their higher-preference projects.
5. **Fairness and Diversity Considerations:** Incorporating fairness and diversity considerations, such as ensuring equitable access to popular projects or balancing project assignments to promote diversity, could enhance the social utility of the matching.
6. **Iterative Feedback and Re-Matching:** Implementing an iterative process where students and projects can provide feedback on tentative matches before finalizing them, allowing for adjustments based on additional information or changed preferences.
7. **Algorithm Efficiency:** Improving the computational efficiency of the algorithm to handle larger datasets more quickly, possibly by optimizing the data structures used or by implementing more efficient sorting and matching methods.
8. **Post-Matching Analysis Tools:** Providing tools for analyzing the results of the matching process, such as identifying unmatched students or projects with unfulfilled capacities, could help administrators make informed decisions about how to adjust the process or address mismatches.

   
