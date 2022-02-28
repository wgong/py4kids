using System;

class Program
{
  enum Level
  {
    Low,
    Medium,
    High
  }
  static void Main(string[] args)
  {
    Level myVar = Level.Medium;
    Console.WriteLine(myVar);


    // Error handling
    try {
	int[] myNumbers = {1, 2, 3};
  	Console.WriteLine(myNumbers[10]);
    } catch (Exception e) {
    	Console.WriteLine(e.Message);
    }
  }
}
