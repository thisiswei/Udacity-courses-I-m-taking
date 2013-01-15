is_older((1987,12,13), (1987,12,14)) = true;  

number_in_month([(1987,12,13), (1987,12,14)], 12) = 2;

number_in_months([(1987,12,13), (1987,12,14), (1987,10,13)], [10, 12]) = 3;

dates_in_month([(1234,12,1),(1223,10,1)], 10) = [(1223,10,1)];

dates_in_months([(1234,12,1),(1223,10,1)], [10,12]) = [(1223,10,1),(1234,12,1)];
  
get_nth(["wtf","mutherfucker","I","can","doit","myself"], 3) = "I"; 
  
date_to_string((2, 20, 2012)) = "February 20 2012" ;
  
number_before_reaching_sum(8, [1,2,4,5,6]) = 3; 
  
number_before_reaching_sum(12, [1,2,4,5,6]) = 4; 
  
what_month(33) = 2; 
  
month_range(28, 39) = [1,1,1,2,2,2,2,2,2,2,2,2]; 

        
