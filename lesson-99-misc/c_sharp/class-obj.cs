using System;

class Car
{
  public string model;
  public string color;
  public int year;
  string owner;


  // Create a class constructor with multiple parameters
  public Car(string modelName, string modelColor, int modelYear)
  {
    model = modelName;
    color = modelColor;
    year = modelYear;
    owner = owner;
  }


    // short-hand
	public string Owner 
    {get; set;}

    /*
    public string Owner // property
    {
      get { return owner;}
      set { owner = value;}

    }
    */

  static void Main(string[] args)
  {
    Car Ford = new Car("Mustang", "Red", 1969);
    Car Opel = new Car("Astra", "White", 2005);
    
    Console.Write("I have a Ford: ");
    Console.WriteLine(Ford.color + ", " + Ford.year + ", " + Ford.model+ ", " + Ford.Owner);

    Console.Write("He has a Opel: ");
    Opel.Owner = "Jane";
    Console.WriteLine(Opel.color + ", " + Opel.year + ", " + Opel.model + ", " + Opel.Owner);

	}
}
