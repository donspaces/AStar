# A*

![](https://www.101computing.net/wp/wp-content/uploads/A-Star-Search-Algorithm-Step-5.png)
> From https://www.101computing.net/a-star-search-algorithm/
>

## Description

​	A* algorithm is a heuristic search algorithm which use f-value $( f(n) = g(n) + h(n) )$ to guide the search with least-cost first design.



## Terms

$h(n)$ : Heuristic function

$g(n)$ : Cost function

$h^*(n)$ : Optimal Cost to the goal

$g^*(n)$ : Optimal Cost function



## Heuristic Properties

*Admissible*
$$\forall n \in G \quad h(n) \leq h^*(n)$$
*Consistent*
$$\forall n \in G,\ n' \in G \quad\ h(n) - h'(n) \leq cost(n, n')$$




## Heuristics

*Manhattan distance*
$$h(n) = |y_g - y_n| + |x_g - x_n|$$
*Octile distance*
$$h(n) = \sqrt{2}\min(\Delta{y_{gn}}, \Delta{x_{gn}}) + |\Delta{y_{gn}} - \Delta{x_{gn}}|$$
*Euclidean distance*
$$h(n) = \sqrt{(y_g - y_n)^2 + (x_g - x_n)^2}$$


## Pseudocode

```pseudocode
function Astar(S, G):
  define Min-Heap OPEN
  define Hash-Table CLOSE
  OPEN.push(S, h(S))

  while OPEN is not Empty:
    node = OPEN.pop()
    if node == G:
      return Path(S, G), CLOSE[node].g
    else:
      for child in T(node):
        g = CLOSE[node].g + cost(node, child)
        f = g + h(child)
        if child not in CLOSED:
          OPEN.push(child, f)
          CLOSE.append(child)
          CLOSE[child].g = g
          CLOSE[child].f = f
        if child in CLOSED and child.f < CLOSE[child].f:
          CLOSE[child].g = g
          CLOSE[child].f = f

    return -1
```



