using System;

class Animal  // Base class (parent) 
{
  public void makeSound() 
  {
    Console.WriteLine("The animal makes a sound");
  }
}

class Pig : Animal  // Derived class (child) 
{
  public void makeSound() 
  {
    Console.WriteLine("The pig says: wee wee");
  }
}

class Dog : Animal  // Derived class (child) 
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

	Animal anim = new Animal();
    anim.makeSound();

	Pig pig = new Pig();
    pig.makeSound();

	Dog dog = new Dog();
    dog.makeSound();


  }
}
