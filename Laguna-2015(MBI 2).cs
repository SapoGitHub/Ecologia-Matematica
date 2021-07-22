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
        public List<Agente> agentes = new List<Agente>();  //Lista de todos os agentes
        public List<Agente> vizinhos = new List<Agente>(); //Lista de todos os agentes proximos
        public List<Agente> prole = new List<Agente>();    //Lista pra guardar a prole

        //Agente
        public bool extinto = false;                       //Se o a gente foi extinto
        public string nome;                                //Que tipo de agente é
        public int x;                                      //Posição x                   
        public int y;                                      //Posição y
        public double ext;                                 //Taxa de extinção       
        public double my;                                  //Taxa de predação
        public double col;                                 //Taxa de colonização

        //Configurações
        const string guanaco = "Guanaco";
        const string ovelha = "Ovelha";
        const string puma = "Puma";
        public Random ale;                                  //Semente dos números aleatórios

        //Criação do agente
        //public Agente(){ }
        public void Predar()
        {
            foreach (Agente A in vizinhos)
            {
                if (A.x==x && A.y==y && A.extinto==false) //&& (A.nome == guanaco || A.nome == ovelha)
                {
                    double rnd = ale.NextDouble();
                    A.extinto = (rnd < A.my);
                }
            }
        }
        //Método para causar o deslocamento competitivo
        public void Deslocamento()
        {
            foreach (Agente A in vizinhos)
            {
                if (A.x == x && A.y == y && A.extinto == false && (A.nome==ovelha))
                {
                    double rnd = ale.NextDouble();
                    A.extinto = (rnd < col);
                }
            }
        }
        //Método ser extindo localmente
        public void Extincao()
        {
            double rnd = ale.NextDouble();
            extinto = (rnd < ext);
        }
        //Método para avalizar a vizinhança
        public void Vizinhanca()
        {
            vizinhos = new List<Agente>();
            vizinhos = agentes.FindAll((Agente A) => (Math.Abs(A.x - x) + Math.Abs(A.y - y)) <= 1 && (A!=this));
        }
        //Método para colonizar
        public void Colonizar()
        {
            double rnd = ale.NextDouble();
            if (s[x - 1, y] == 1 && rnd < col) { Col_Sup(this, x - 1, y); }
            rnd = ale.NextDouble();
            if (s[x + 1, y] == 1 && rnd < col) { Col_Sup(this, x + 1, y); }
            rnd = ale.NextDouble();
            if (s[x, y - 1] == 1 && rnd < col) { Col_Sup(this, x, y - 1); }
            rnd = ale.NextDouble();
            if (s[x, y + 1] == 1 && rnd < col) { Col_Sup(this, x, y + 1); }
        }
        static void Col_Sup(Agente pai, int x, int y)
        {
            bool gua, ove, pum;
            bool c = true;

            switch (pai.nome)
            {
                case guanaco: //Não pode estar ocupado por si mesmo
                    gua = pai.vizinhos.Exists((Agente A) => (A.nome == guanaco && A.x == x && A.y == y));
                    if (gua == false)  //Para não gerar 2 indivíduos no mesmo espaço
                    {
                        gua= pai.prole.Exists((Agente A) => (A.nome == guanaco && A.x == x && A.y == y));
                        c = (gua == false);
                    }
                    else { c = false; }
                    break;
                case ovelha:
                    gua = pai.vizinhos.Exists((Agente A) => (A.nome == guanaco && A.x == x && A.y == y));
                    ove = pai.vizinhos.Exists((Agente A) => (A.nome == ovelha  && A.x == x && A.y == y));
                    if (gua == false && ove == false) //Para não gerar 2 indivíduos no mesmo espaço
                    {
                        ove = pai.prole.Exists((Agente A) => (A.nome == ovelha && A.x == x && A.y == y));
                        c = (gua == false);
                    }
                    else { c = false; }
                    break;
                case puma:
                    int ocup = 0;
                    gua = pai.vizinhos.Exists((Agente A) => (A.nome == guanaco && A.x == x && A.y == y));
                    ove = pai.vizinhos.Exists((Agente A) => (A.nome == ovelha  && A.x == x && A.y == y));
                    pum = pai.vizinhos.Exists((Agente A) => (A.nome == puma   && A.x == x && A.y == y));
                    ocup += (gua == true || ove == true) ? 1 : 0;
                    if(pum == false && ocup == 1) //Para não gerar 2 indivíduos no mesmo espaço
                    {
                        pum  = pai.prole.Exists((Agente A) => (A.nome == puma && A.x == x && A.y == y));
                        c = (pum == false);
                    }
                    else { c = false; }
                    break;
            }
             if (c == true)
            {
                Agente ag = new Agente() { s = pai.s, x = x, y = y, nome = pai.nome, ext = pai.ext, my = pai.my, col = pai.col, agentes = pai.agentes, prole = pai.prole, ale = pai.ale };
                pai.prole.Add(ag);
            }
        }
    }

    class Modelo
    {
        //Mundo
        private const int maxit = 6000;                            //Número de iterações
        private const int Lx = 100;                                 //Tamanho no eixo x
        private const int Ly = 100;                                 //Tamanho no eixo y
        private readonly List<Agente> Agentes = new List<Agente>(); //Lista de agentes
        private readonly List<Agente> prole = new List<Agente>();   //lista de prole

        //Fracciones iniciales
        private const double D   = 0.3;                          //fraccion inicial de sitios destruidos
        private const double x10 = 0.5;                          //Probabilidade da grade ser ocupada por x1
        private const double x20 = 0.5;                          //Probabilidade da grade ser ocupada por x2
        private const double y0  = 0.5;                          //Probabilidade de nascer um predador junto da presa    
        
        //Tasas               
        private const double cx1 = 0.050;                          //colonizaciones       
        private const double cx2 = 0.100; // cx2  >  cx1
        private const double cy = 0.015;
        private const double ex1 = 0.050;                          //extinciones       
        private const double ex2 = 0.010; // ex2  <  ex1
        private const double ey = 0.017;
        private const double mx1y = 0.200;                          //depredaciones       
        private const double mx2y = 0.800; // mx2y >> mx1y

         //Configurações
        private const string guanaco = "Guanaco";
        private const string ovelha = "Ovelha";
        private const string puma = "Puma";
        private readonly Random ale = new Random();                                   //Semente dos números aleatórios

        public Modelo() //Construtor
        {
            //Configurar o estado inicial
            int[,] s = new int[Lx, Ly];                 //Na verdade é [linha, coluna], então está invertido
            for (int i = 1; i < Lx - 1; i++)
            {
                for (int j = 1; j < Ly - 1; j++)
                {
                    bool p = false, g = false;
                    double rnd = ale.NextDouble();
                    s[i, j] = (rnd < D) ? 0 : 1;    //Destroi ou não o fragmento
                    rnd = ale.NextDouble();
                    if (rnd < x10 && s[i, j] == 1)  //Gera guanaco
                    {
                        Agente ag = new Agente() { s = s, x = i, y = j, nome = guanaco, ext = ex1, my = mx1y, col = cx1, agentes = Agentes, prole = prole,ale = ale };
                        Agentes.Add(ag);
                        p = true;
                    }
                    rnd = ale.NextDouble();
                    if (rnd < x20 && s[i, j] == 1)  //Guera ovelha
                    {
                        Agente ag = new Agente() { s = s, x = i, y = j, nome = ovelha , ext = ex2, my = mx2y, col = cx2, agentes = Agentes, prole = prole, ale = ale };
                        Agentes.Add(ag);
                        p = true;
                    }
                    rnd = ale.NextDouble();
                    if ((p || g) && (rnd < y0))
                    {
                        Agente ag = new Agente() { s = s, x = i, y = j, nome = puma   , ext = ey , my = 0  , col = cy  , agentes = Agentes, prole = prole, ale = ale };
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
                foreach (Agente A in Agentes){ A.Vizinhanca();}         //Reconhecer os vizinhos
                foreach (Agente A in Agentes){ A.Colonizar(); }         //Coloniza as posições vizinhas
                foreach (Agente A in Agentes) { A.Extincao(); }
                foreach (Agente A in Agentes) { if (A.nome==puma) { A.Predar(); } }
                foreach (Agente A in Agentes) { if (A.nome == guanaco) { A.Deslocamento(); } }
                Agentes.RemoveAll((Agente obj) => obj.extinto == true);  //Removemos os agentes que foram predados
                Agentes.AddRange(prole);                                 //Adiciona a prole 
                prole.Clear();                                           //Limpa a lista de prole
                Registro(Lx, Ly, Agentes, it + 1);                       //registra
            }
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
                y  += (A.nome == puma) ? 1 : 0;
            }
            //Normalizar pra fração de fragmentos da grade
/*            x1 /= (Lx - 1) * (Ly - 1);
            x2 /= (Lx - 1) * (Ly - 1);
            y /= (Lx - 1) * (Ly - 1);*/
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