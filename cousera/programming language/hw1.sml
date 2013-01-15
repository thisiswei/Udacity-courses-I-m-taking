

fun is_older(x: int*int*int, y:int*int*int) = 
    if #1 x < #1 y orelse (#1 x = #1 y andalso (#2 x < #2 y orelse #3 x < #3 y))
    then true
    else false

fun number_in_month(x: (int*int*int) list, y: int) =
    if null x
    then 0
    else if #2 (hd x) <> y
    then 0 + number_in_month((tl x), y)
    else 1 + number_in_month((tl x), y)

fun number_in_months(x: (int*int*int) list, y: int list) =
    if (tl y) = []
    then number_in_month(x, (hd y))
    else number_in_month(x, (hd y)) + number_in_months(x, (tl y))


fun dates_in_month(x: (int*int*int) list, y: int) =
    if null x
    then []
    else if #2 (hd x) = y
    then hd x :: dates_in_month((tl x), y)
    else dates_in_month((tl x), y)

fun dates_in_months(x: (int*int*int) list, y: int list) =
    if (tl y) = []
    then dates_in_month(x, (hd y))
    else dates_in_month(x, (hd y)) @ dates_in_months(x, (tl y))

fun get_nth(x: string list, y: int) = 
    if y = 1
    then hd x
    else get_nth((tl x), y-1)


val months = ["January", "February", "March", "April","May", "June", "July",
"August", "September", "October", "November", "December"];

fun date_to_string(x: int*int*int) = 
    get_nth(months, (#1 x)) ^ " "
           ^ Int.toString(#2 x) ^ " "
           ^ Int.toString(#3 x)

fun number_before_reaching_sum(x: int, y: int list) = 
    if null y orelse  x - (hd y) < 0
    then 0
    else 1 + (number_before_reaching_sum((x-(hd y)), (tl y)))

val daysinmonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

fun what_month(x: int) = 1 + number_before_reaching_sum(x, daysinmonths)  
     
fun month_range(x: int, y: int) = 
    if x > y
    then []
    else what_month(x) :: month_range(x+1, y)



    
    
(* dates_in_months([(1234,12,1),(1223,10,1)], [10,12]); *)
(* get_nth(["wtf","mutherfucker","I","can","doit","myself"], 3); *)
(* date_to_string((2, 20, 2012)); *)
(* number_before_reaching_sum(8, [1,2,4,5,6]); *)
(* number_before_reaching_sum(12, [1,2,4,5,6]); *)
(* what_month(33); *) 
(* month_range(28, 39); *)
