using System;
using System.Data;
using System.IO;
using System.Linq;
using MySql.Data.MySqlClient;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace haplon
{
    class Program
    {
        static void Main(string[] args)
        {
            // Connection with the database
            MySqlConnection conn = new MySqlConnection("server=localhost;database=hoplon;uid=root;pwd=admin");
            conn.Open();

            if (conn.State == ConnectionState.Open)
            {
                Console.WriteLine("Connection Opened Successfully");
            }

            // Loop through the following folder and read each file with .txt extension
            var folderPath = "events/";
            foreach (string file in Directory.EnumerateFiles(folderPath, "*.txt"))
                {
                    try
                    {
                        // Read each file and transform the lines into lists
                        string contents = File.ReadAllText(file);
                        List<string> listStrLineElements = contents.Split(new string[] { Environment.NewLine }, StringSplitOptions.None).ToList();
                        List<string> rowList = listStrLineElements.SelectMany(s => s.Split(' ')).ToList();

                        // Loop through the data, transform and load it to insert each line into the database
                        for (int i = 0; i <= rowList.Count -5; i += 5)
                            {
                                // Transform the data so it can be inserted into the database appropriately
                                var actionDate = rowList[i];
                                var actionTime = rowList[i + 1].Split(',')[0].Trim();
                                var dicString = rowList[i + 4];
                                var dic = JsonConvert.DeserializeObject<Dictionary<string, string>>(dicString);

                                // Insert the data into the database
                                MySqlCommand cmd = null;
                                string cmdString = "";
                                cmdString = ("INSERT INTO game_server_logs (actionDate, actionTime, action, userId) " +
                                String.Format("Values ('{0}','{1}','{2}','{3}')", actionDate, actionTime, dic["Action"], dic["UserID"]));
                                cmd = new MySqlCommand(cmdString, conn);
                                cmd.ExecuteNonQuery();
                            }
                        Console.WriteLine("\n");
                    }
                    catch (IOException e)
                    {
                        Console.WriteLine("The file could not be read:");
                        Console.WriteLine(e.Message);
                    }


                }  
            
            // Close the connection with the database
            conn.Close();
    }
}
}
