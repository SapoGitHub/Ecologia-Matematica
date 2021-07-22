/*
Modelo baseado em autômato celular com orientação a objetos
Autor:           Jhordan Silveira de Borba
E-mail:          sbjhordan @gmail.com
Site:            https://sites.google.com/view/jdan/
*/

using System;                     //Namespace padrão System
using System.Collections.Generic; //Para usar listas
using System.IO;                  //include the System.IO namespace
using System.Globalization;       //Mudar a cultura (pontuação)

namespace Vida_selvagem_e_Pecuária
{
    class Agente
    {
        //Mundo
        public int[,] s;                                   //Marcar os fragmentos destruídos                      

        //Agente
        public bool extinto = false;                       //Se o a gente foi extinto
        public string nome;                                //Que tipo de agente é
        public int x;                                      //Posição x                   
        public int y;                                      //Posição y
        public double ext;                                 //Taxa de extinção       
        public double my;                                  //Taxa de predação

        //Configurações
        const string guanaco = "Guanaco";
        public StreamReader file;

        //Criação do agente
        //public Agente(){ }
        public void Predar()
        {
            double dep = ext + my;
            double rnd = Convert.ToDouble(file.ReadLine());
            extinto = (rnd < dep);
        }
        //Método para causar o deslocamento competitivo
        public void Deslocamento()
        {
            double rnd = Convert.ToDouble(file.ReadLine());
            //Agente ag = agentes.Find((Agente A) => (A.nome == guanaco && A.x == x && A.y == y));
            extinto = (rnd < 0.05 || extinto == true);
        }
        //Método ser extindo localmente
        public void Extincao()
        {
            double rnd = Convert.ToDouble(file.ReadLine());
            extinto = (rnd < ext);
        }
        //Método para deslocar
        //Método para colonizar
    }

    class Modelo
    {
        private const int maxit = 15000;                            //Número de iterações
        private const int Lx = 100;                                 //Tamanho no eixo x
        private const int Ly = 100;                                 //Tamanho no eixo y
        private readonly List<Agente> Agentes = new List<Agente>(); //Lista de agentes
        private readonly List<Agente> prole = new List<Agente>();   //lista de prole

        //Fracciones iniciales
        private const double D   = 0.3;                          //fraccion inicial de sitios destruidos
        private const double x10 = 0.5;                          //Probabilidade da grade ser ocupada por x1
        private const double x20 = 0.5;                          //Probabilidade da grade ser ocupada por x2
        private const double y0  = 0.5;                          //Probabilidade de nascer um predador junto da presa    
        //A probabilidade de ser y é y0=1-x1-x2
        //Tasas               
        private const double cx1 = 0.050;                          //colonizaciones       
        private const double cx2 = 0.100; // cx2  >  cx1
        private const double cy = 0.015;
        private const double ex1 = 0.050;                          //extinciones       
        private const double ex2 = 0.010; // ex2  <  ex1
        private const double ey = 0.017;
        private const double mx1y = 0.200;                          //depredaciones       
        private const double mx2y = 0.800; // mx2y >> mx1y

        private readonly StreamReader file = new StreamReader("psd.dat");  //Método para ler arquivos

        //Garantir que os nomes das espécies estão corretos
        private const string guanaco = "Guanaco";
        private const string ovelha = "Ovelha";
        private const string puma = "Puma";

        public Modelo() //Construtor
        {
            //Configurar o estado inicial
            int[,] s = new int[Lx, Ly];                 //Na verdade é [linha, coluna], então está invertido
            for (int i = 1; i < Lx - 1; i++)
            {
                for (int j = 1; j < Ly - 1; j++)
                {
                    bool p = false, g = false;
                    double rnd = Convert.ToDouble(file.ReadLine());
                    s[i, j] = (rnd < D) ? 0 : 1;    //Destroi ou não o fragmento
                    rnd = Convert.ToDouble(file.ReadLine());
                    if (rnd < x10 && s[i, j] == 1)  //Gera guanaco
                    {
                        Agente ag = new Agente() { s = s, file = file, x = i, y = j, nome = guanaco, ext = ex1, my = mx1y};
                        Agentes.Add(ag);
                        p = true;
                    }
                    rnd = Convert.ToDouble(file.ReadLine());
                    if (rnd < x20 && s[i, j] == 1)  //Guera ovelha
                    {
                        Agente ag = new Agente() { s = s, file = file, x = i, y = j, nome = ovelha, ext = ex2, my = mx2y};
                        Agentes.Add(ag);
                        p = true;
                    }
                    rnd = Convert.ToDouble(file.ReadLine());
                    if ((p || g) && (rnd < y0))
                    {
                        Agente ag = new Agente() { s = s, file = file, x = i, y = j, nome = puma, ext = ey, my = 0};
                        Agentes.Add(ag);
                    }
                    p = g = false;
                }
            }

            Registro(Lx, Ly, Agentes, 0);                               //Registra
            //Laço temporal
            for (int it = 0; it < maxit; it++)                          //Roda a simulação
            {
                Console.WriteLine(it);
                for (int i = 1; i < Lx - 1; i++)
                {
                    for (int j = 1; j < Ly; j++)
                    {
                        //Colonizações
                        //Guanaco
                        Agente guan = Agentes.Find((Agente A) => (A.nome == guanaco && A.x == i && A.y == j));
                        if (guan == null && s[i, j] == 1)
                        {
                            int nvec = 0;
                            Agente obj1 = Agentes.Find((Agente A) => (A.nome == guanaco && A.x - 1 == i && A.y == j));
                            Agente obj2 = Agentes.Find((Agente A) => (A.nome == guanaco && A.x + 1 == i && A.y == j));
                            Agente obj3 = Agentes.Find((Agente A) => (A.nome == guanaco && A.x == i && A.y == j - 1));
                            Agente obj4 = Agentes.Find((Agente A) => (A.nome == guanaco && A.x == i && A.y == j + 1));
                            nvec += (obj1 != null) ? 1 : 0;
                            nvec += (obj2 != null) ? 1 : 0;
                            nvec += (obj3 != null) ? 1 : 0;
                            nvec += (obj4 != null) ? 1 : 0;
                            double p = 1 - Math.Pow((1.0 - cx1), nvec);
                            double rnd = Convert.ToDouble(file.ReadLine());
                            if (rnd < p)
                            {
                                Agente ag = new Agente() { s = s, file = file, x = i, y = j,  nome = guanaco, ext = ex1, my = mx1y};
                                prole.Add(ag);
                            }
                        }
                        //Ovelha
                        Agente ove = Agentes.Find((Agente A) => (A.nome == ovelha && A.x == i && A.y == j));
                        if (ove == null && guan == null && s[i, j] == 1)
                        {
                            int nvec = 0;
                            Agente obj1 = Agentes.Find((Agente A) => (A.nome == ovelha && A.x - 1 == i && A.y == j));
                            Agente obj2 = Agentes.Find((Agente A) => (A.nome == ovelha && A.x + 1 == i && A.y == j));
                            Agente obj3 = Agentes.Find((Agente A) => (A.nome == ovelha && A.x == i && A.y == j - 1));
                            Agente obj4 = Agentes.Find((Agente A) => (A.nome == ovelha && A.x == i && A.y == j + 1));
                            nvec += (obj1 != null) ? 1 : 0;
                            nvec += (obj2 != null) ? 1 : 0;
                            nvec += (obj3 != null) ? 1 : 0;
                            nvec += (obj4 != null) ? 1 : 0;
                            double p = 1 - Math.Pow((1.0 - cx2), nvec);
                            double rnd = Convert.ToDouble(file.ReadLine());
                            if (rnd < p)
                            {
                                Agente ag = new Agente() { s = s, file = file, x = i, y = j, nome = ovelha, ext = ex2, my = mx2y};
                                prole.Add(ag);
                            }
                        }
                        //Puma
                        Agente pum = Agentes.Find((Agente A) => (A.nome == puma && A.x == i && A.y == j));
                        int ocup = 0;
                        ocup = (guan != null || ove != null) ? 1 : 0;
                        if (pum == null && ocup == 1)
                        {
                            int nvec = 0;
                            Agente obj1 = Agentes.Find((Agente A) => (A.nome == puma && A.x - 1 == i && A.y == j));
                            Agente obj2 = Agentes.Find((Agente A) => (A.nome == puma && A.x + 1 == i && A.y == j));
                            Agente obj3 = Agentes.Find((Agente A) => (A.nome == puma && A.x == i && A.y == j - 1));
                            Agente obj4 = Agentes.Find((Agente A) => (A.nome == puma && A.x == i && A.y == j + 1));
                            nvec += (obj1 != null) ? 1 : 0;
                            nvec += (obj2 != null) ? 1 : 0;
                            nvec += (obj3 != null) ? 1 : 0;
                            nvec += (obj4 != null) ? 1 : 0;
                            double p = 1 - Math.Pow((1.0 - cy), nvec);
                            double rnd = Convert.ToDouble(file.ReadLine());
                            if (rnd < p)
                            {
                                Agente ag = new Agente() { s = s, file = file, x = i, y = j, nome = puma, ext = ey, my = 0};
                                prole.Add(ag);
                            }
                        }
                        //Extinção sem predador
                        //Guanaco
                        if (guan != null && pum == null) { guan.Extincao(); }
                        //Ovelha
                        if (ove != null && pum == null) { ove.Extincao(); }
                        //Puma
                        if (pum != null) { pum.Extincao(); }
                        //Depredacao
                        //Guanaco
                        if (guan != null && pum != null) { guan.Predar(); }
                        //Ovelha
                        if (ove != null && pum != null) { ove.Predar(); }
                        //Deslocamento
                        if (ove != null && guan != null) { ove.Deslocamento(); }
                    }
                }
                Agentes.RemoveAll((Agente obj) => obj.extinto == true);  //Removemos os agentes que foram predados
                Agentes.AddRange(prole);                                 //Adiciona a prole 
                prole.Clear();                                           //Limpa a lista de prole
                Registro(Lx, Ly, Agentes, it + 1);                            //registra
            }
            file.Close();
        }
        //Métodos auxiliares
        static void Registro(int Lx, int Ly, List<Agente> Agentes, int i)
        {
            //Guardar a quantidade de cada espécie
            double x1 = 0;
            double x2 = 0;
            double y = 0;
            foreach (Agente A in Agentes)
            {
                x1 += (A.nome == guanaco) ? 1 : 0;
                x2 += (A.nome == ovelha) ? 1 : 0;
                y += (A.nome == puma) ? 1 : 0;
            }
            //Normalizar pra fração de fragmentos da grade
            x1 /= (Lx - 1) * (Ly - 1);
            x2 /= (Lx - 1) * (Ly - 1);
            y /= (Lx - 1) * (Ly - 1);
            File.AppendAllText("Dados.dat", "\t" + i + "\t" + x1 + "\t" + x2 + "\t" + y + "\n");
        }
    }

    class Program
    {
        static void Main()
        {
            CultureInfo.CurrentCulture = new CultureInfo("en-US"); //Mudamos a cultura
            new Modelo();       //Inicia o modelo
            Console.WriteLine("Acabou meu chapinha.");
            Console.ReadKey();
        }
    }
}