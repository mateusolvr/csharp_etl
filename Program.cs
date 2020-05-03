using System;
using System.IO;

namespace haplon
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
            var folderPath = "events/";
            foreach (string file in Directory.EnumerateFiles(folderPath, "*.txt"))
                {
                    try
                    {
                        string contents = File.ReadAllText(file);
                        Console.WriteLine(contents);
                    }
                    catch (IOException e)
                    {
                        Console.WriteLine("The file could not be read:");
                        Console.WriteLine(e.Message);
                    }


                }                          
    }
}
}
