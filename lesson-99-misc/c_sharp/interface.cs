using System;

// Interface
interface IAnimal 
{
  void makeSound(); // interface method (does not have a body)
}


class Pig : IAnimal  // Pig "implements" the IAnimal interface
{
  public void makeSound() 
  {
    Console.WriteLine("The pig says: wee wee");
  }
}

class Dog : IAnimal  // Dog "implements" the IAnimal interface
{
  public void makeSound() 
  {
    Console.WriteLine("The dog says: bow wow");
  }
}

class Program
{
  static void Main(string[] args)
  {


	Pig pig = new Pig();
    pig.makeSound();

	Dog dog = new Dog();
    dog.makeSound();


  }
}
