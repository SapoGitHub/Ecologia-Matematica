using System;               //Namespace padrão System
using System.IO;            // include the System.IO namespace
using System.Globalization; //Mudar a cultura (pontuação)


namespace Vida_selvagem_e_Pecuária
{
    class Program
    {
        static double[] Densidade (int[,] x1, int[,] x2, int[,] y, int Lx, int Ly) //Static para ser acesssível sem ser objeto
        {
            double[] f = { 0, 0, 0 };
            for (int i = 1; i < Lx-1; i++)
            {
                for (int j = 1; j < Ly-1; j++)
                {
                    f[0] = f[0] + x1[i, j];
                    f[1] = f[1] + x2[i, j];
                    f[2] = f[2] + y[i, j];
                }
            }
            f[0] /= (Lx - 2) * (Ly - 2);
            f[1] /= (Lx - 2) * (Ly - 2);
            f[2] /= (Lx - 2) * (Ly - 2);
            return f;
        }
        static void Main(string[] args)
        {
            CultureInfo.CurrentCulture = new CultureInfo("en-US"); //Mudamos a cultura

            //Condições iniciais
            int maxt = 5000; //Tempo total de cada realização
            int   Lx = 100;   //Tamanho na dimensão X
            int   Ly = 100;   //Tamanho na dimensão y

            //Frações iniciais
            double D   = 0.3;
            double x10 = 0.5;
            double x20 = 0.5;
            double y0  = 0.5;

            //Taxas
            double cx1   = 0.05;
            double cx2   = 0.1;
            double cy    = 0.015;
            double ex1   = 0.05;
            double ex2   = 0.01;
            double ey    = 0.017;
            double mx1y  = 0.2;
            double mx2y = 1 - ex2;
            double depx1 = ex1+mx1y;
            double depx2 = ex2+mx2y;

            Random rnd = new Random(); //Gerador de número aleatório alimentado pelo sistema

            //Inicializa as matrizes
            int[,] s  = new int[Lx, Ly];
            int[,] x1 = new int[Lx, Ly];
            int[,] x2 = new int[Lx, Ly];
            int[,] y  = new int[Lx, Ly];

            for (int i = 1; i < Lx-1; i++)
            {
                for (int j=1; j<Ly-1;j++)
                {
                     s[i,j] = (rnd.NextDouble() < D) ? 0 : 1;
                    x1[i,j] = (rnd.NextDouble() < x10 && s[i,j] == 1) ? 1 : 0;
                    x2[i,j] = (rnd.NextDouble() < x20 && s[i,j] == 1) ? 1 : 0;
                    y[i, j] = ((x1[i,j]==1||x2[i,j]==1)&&(rnd.NextDouble() < y0)) ? 1 : 0;
                }
            }
            //Laço temporal
            double[] f=Program.Densidade(x1, x2, y, Lx, Ly);
            File.AppendAllText("Dados.dat","\t"+0+"\t"+f[0] + "\t"+ f[1] + "\t"+ f[2] + "\n");
            Console.WriteLine("\t" + 0 + "\t" + f[0] + "\t" + f[1] + "\t" + f[2] + "\n");

            for (int it=0;it<maxt;it++)
            {
                int[,] x1old = x1.Clone() as int[,];
                int[,] x2old = x2.Clone() as int[,];
                int[,] yold  =  y.Clone() as int[,];

                //Percorrer a malha
                for (int i=1; i<Lx-1; i++)
                {
                    for (int j=1; j<Ly-1; j++)
                    {
                        //Colonizações
                        //Guanaco
                        if (x1old[i, j] == 0 && s[i, j] == 1)
                        {
                            int nvec = x1old[i - 1, j] + x1old[i + 1, j] + x1old[i, j - 1] + x1old[i, j + 1];
                            double p = 1 - Math.Pow((1.0 - cx1), nvec);
                            x1[i, j] = (rnd.NextDouble() < p) ? 1 : x1[i, j];
                        }
                        //Ovelha
                        if (x1old[i, j] == 0 && x2old[i,j]==0 && s[i, j] == 1)
                        {
                            int nvec = x2old[i - 1, j] + x2old[i + 1, j] + x2old[i, j - 1] + x2old[i, j + 1];
                            double p = 1 - Math.Pow((1.0 - cx2), nvec);
                            x2[i, j] = (rnd.NextDouble() <p) ? 1 : x2[i, j];
                        }
                        //Puma
                        int ocup = (x1old[i, j] == 1 || x2old[i, j] == 1) ? 1 : 0;
                        if (yold[i,j]==0 && ocup==1)
                        {
                            int nvec = yold[i - 1, j] + yold[i + 1, j] + yold[i, j - 1] + yold[i, j + 1];
                            double p = 1 - Math.Pow((1.0 - cy), nvec);
                            y[i, j] = (rnd.NextDouble() < p) ? 1 : y[i, j];
                        }
                        //Extinção sem predador
                        //Guanaco
                        if(x1old[i,j]==1 && yold[i,j]==0)
                        {x1[i, j] = (rnd.NextDouble() < ex1) ? 0 : x1[i, j]; }
                        //Ovelha
                        if(x2old[i,j]==1 && yold[i, j]==0)
                        {x2[i, j] = (rnd.NextDouble() < ex2) ? 0 : x2[i, j]; }
                        //Puma
                        if (yold[i, j] == 1)
                        {y[i, j]  = (rnd.NextDouble() <  ey) ? 0 : y[i, j]; }
                        //Depredação
                        //Guanaco
                        if (x1old[i, j] == 1 && yold[i, j] == 1)
                        {x1[i, j] = (rnd.NextDouble() < depx1) ? 0 : x1[i, j]; }
                        //Ovelha
                        if (x2old[i, j] == 1 && yold[i, j] == 1)
                        {x2[i, j] = (rnd.NextDouble() < depx2) ? 0 : x2[i, j];}
                        //Deslocamento
                        if (x1old[i, j] == 1 && x2old[i, j] == 1)
                        {x2[i, j] = (rnd.NextDouble() < cx1) ? 0 : x2[i, j]; }
                    }
                }
                f = Program.Densidade(x1, x2, y, Lx, Ly);
                File.AppendAllText("Dados.dat","\t" +(it+1) + "\t" + f[0] + "\t" + f[1] + "\t" + f[2] + "\n");
            }
            Console.WriteLine("\t" + 0 + "\t" + f[0] + "\t" + f[1] + "\t" + f[2] + "\n");
            Console.ReadKey();
        }
    }
}

/*
 Depois edito pra ver se funciona linha a linha
 * int counter = 0;  
string line;  
  
// Read the file and display it line by line.  
System.IO.StreamReader file =
    new System.IO.StreamReader(@"c:\test.txt");  
while((line = file.ReadLine()) != null)  
{  
    System.Console.WriteLine(line);  
    counter++;  
}  
  
file.Close();  
System.Console.WriteLine("There were {0} lines.", counter);  
// Suspend the screen.  
System.Console.ReadLine(); */