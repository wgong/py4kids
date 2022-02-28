using System;
using System.Linq;

/*
Learn C# at https://www.w3schools.com/cs/cs_classes.php
*/
namespace ExampleApp
{
  class Program
  {
    // named Args
  static void YoungestKid(string child1, string child2, string child3) 
  {
    Console.WriteLine("The youngest child is: " + child3);
  }    
  
  // method overload

  static int PlusMethod(int x, int y)
  {
    return x + y;
  }

  static double PlusMethod(double x, double y)
  {
    return x + y;
  }

  static string PlusMethod(string x, string y)
  {
    return x + " " + y;
  }

	static void Main(string[] args)
    {
        Console.WriteLine("Sort string array: ");
      string[] cars = {"Matrix", "Volvo", "BMW", "Ford", "Mazda"};
      Array.Sort(cars);
      for (int i = 0; i < cars.Length; i++) 
      {
        Console.WriteLine(cars[i]);
      }
      
        Console.WriteLine("Sort number array: ");
      
      int[] nums = {-1, 100, 51, 13, 1001};
      Array.Sort(nums);
      for (int i = 0; i < nums.Length; i++) 
      {
        Console.WriteLine(nums[i]);
      }

        Console.WriteLine("array: min, max, sum: ");
        Console.WriteLine($"min = {nums.Min()}");
        Console.WriteLine($"min = {nums.Max()}");
        Console.WriteLine($"min = {nums.Sum()}");

		
        // call method with named args
        YoungestKid(child3: "John", child1: "Jane", child2: "Josef");


		// test overload
        
        /*
        int x = 10; int y=20;
        Console.WriteLine($" {x} + {y} = {PlusMethod(x, y)}");

        double x = 10.0011; double y=20.000022 ;
        Console.WriteLine($" {x} + {y} = {PlusMethod(x, y)}");

		*/
        
        string x = "Joe"; string y = "Plumber" ;
        Console.WriteLine($" {x} + {y} = {PlusMethod(x, y)}");

    }
    
  

  }
}
