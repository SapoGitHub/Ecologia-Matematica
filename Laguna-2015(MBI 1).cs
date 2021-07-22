/*
Tentativa de modelo baseado em indivíduo #1
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
        public int[,] s;                                    //Marcar os fragmentos destruídos                      
        public bool extinto = false;                        //Se o a gente foi extinto
        public Random ale;                                  //Semente dos números aleatórios
        public string nome;                                 //Que tipo de agente é
        public int x;                                       //Posição x                   
        public int y;                                       //Posição y
        public List<Agente>  agentes = new List<Agente>();  //Lista de todos os agentes
        public List<Agente> vizinhos = new List<Agente>(); //Lista de todos os agentes proximos
        public List<Agente>  prole = new List<Agente>();    //Lista pra guardar a prole
        public double col;                                  //Taxa de colonização       
        public double ext;                                  //Taxa de extinção       
        public double my;                                   //Taxa de predação
        //Garantir que os nomes das espécies estão corretos
        const string guanaco = "Guanaco";
        const string ovelha  = "Ovelha";
        const string puma    = "Puma";
        //Criação do agente
        //public Agente(){}
        //Método para mover o agente
        /*public void Mover()
        {
            //Em qual eixo se movimenta:
            int xx = x;  //Copia da posição antiga em x
            int yy = y;  //Copia da posição antiga em y
            if (ale.NextDouble() < 0.5) {xx += (ale.NextDouble() < 0.5) ? -1 : 1; } //Mover aleatoriamente para os lados
            else                        {yy += (ale.NextDouble() < 0.5) ? -1 : 1; } //Mover aleatoriamente para cima e baixo                      
            if (s[xx, yy] == 0) { return; }                                         //Se o fragmento está destruído
            switch (nome)                                                           //Checa a disponibilidade dependendo da espécie
            {
                case puma:    //Não pode estar ocupado por si
                    foreach (Agente A in vizinhos)
                    { if (A.x == xx && A.y == yy && (A.nome == puma                      )) { return; } }
                    break;
                case guanaco: //Não pode estar por si mesmo
                    foreach(Agente A in vizinhos)
                    { if (A.x == xx && A.y == yy && (A.nome == guanaco                   )) { return; } }  
                    break;
                case ovelha:  //Não pode estar ocupado por guanacos ou si mesmo
                    foreach (Agente A in vizinhos)
                    { if (A.x == xx && A.y == yy && (A.nome == guanaco || A.nome==ovelha )) { return; } }
                    break;
            }
            x = xx;
            y = yy;
        }*/
        //Método para colonizar
        public void Colonizar()
        {
            double p = ale.NextDouble();
            if (s[x - 1, y] == 1 && p < col) //Se o fragmento não está destruído e a colonização teve sucesso
            { Col(this, x - 1, y); }
            p = ale.NextDouble();
            if (s[x + 1, y] == 1 && p < col) //Se o fragmento não está destruído e a colonização teve sucesso
            { Col(this, x + 1, y); }
            p = ale.NextDouble();
            if (s[x, y - 1] == 1 && p < col) //Se o fragmento não está destruído e a colonização teve sucesso
            { Col(this, x, y - 1); }
            p = ale.NextDouble();
            if (s[x, y + 1] == 1 && p < col) //Se o fragmento não está destruído e a colonização teve sucesso
            { Col(this, x, y + 1); }
        }
        //Método para predar
        public void Predar() 
        {
            foreach(Agente A in vizinhos)
            {   //Lembrando que puma possui predação my=0
                if (A.x == x && A.y == y) 
                {
                    //A.extinto = (ale.NextDouble()<A.my); 
                    double p = ale.NextDouble();
                    if (p < A.my && A.extinto==false)
                    { A.extinto = true; rem.Add(A); }
                } //Se outro vizinho está na mesma posição                                                                                                 //Lembrando que puma possui my=0
            }
        }
        //Método para causar o deslocamento competitivo
        public void Deslocamento() 
        {
            foreach (Agente A in vizinhos)
            {   //Só importa se é ovelha
                if (A.x == x && A.y == y && A.nome==ovelha) 
                {
                    //A.extinto = (ale.NextDouble() < col); 
                    double p = ale.NextDouble();
                    if (p < col && A.extinto == false)
                    { A.extinto = true; rem.Add(A); }
                }
            }
        }
        //Método ser extindo localmente
        public void Extincao() 
        {
            double p = ale.NextDouble();
            if (p< ext && extinto == false)
            { extinto = true; rem.Add(this); }
            //extinto = (ale.NextDouble() < ext); 
        }
        //Funcao para identificar os vizinhos
        public void Vizinhanca() 
        {
            List<Agente> nvi = new List<Agente>();                      //Cria uma nova lista
            foreach (Agente A in agentes)
            {if ((Math.Abs(A.x - x) + Math.Abs(A.y - y)) <= 1 && A!=this) //Se está em uma célula djacente ou a própria, mas não é o próprio agente
                {nvi.Add(A);}}
            vizinhos = nvi;
        }
        //Método auxiliar
        static void Col(Agente pai, int x, int y)
        {
            bool c = true;
            switch (pai.nome)     
            {
                case guanaco: //Não pode estar ocupado por si mesmo
                    foreach (Agente A in pai.vizinhos)                          //Nem atualmente
                    { if (A.x == x && A.y == y && ( A.nome==guanaco                            )) {c = false;break; }}
                    if (c == true)
                    {
                        foreach (Agente A in pai.prole)                             //Nem no futuro
                        { if (A.x == x && A.y == y && (A.nome == guanaco)) { c = false; break; } }
                    }
                    break;
                case ovelha://Não pode ser ocupado por pumas e ovelhas e si mesmo
                    foreach (Agente A in pai.vizinhos)
                    { if (A.x == x && A.y == y && ( A.nome == guanaco || A.nome== ovelha )) {c = false;break; }}
                    if (c== true)
                    {
                        foreach (Agente A in pai.prole)
                        { if (A.x == x && A.y == y && (A.nome == guanaco || A.nome == ovelha)) { c = false; break; } }
                    }
                    break;
                case puma://Precisa ser ocupado por guanacos ou ovelha mas não por pumas
                    c = false;
                    foreach (Agente A in pai.vizinhos)
                    { if (A.x == x && A.y == y && (A.nome == ovelha || A.nome == guanaco )) {c = true; break; }}
                    foreach (Agente A in pai.vizinhos)
                    { if (A.x == x && A.y == y && (A.nome == puma                        )) {c = false;break; }}
                    if (c == true)
                    {
                        foreach (Agente A in pai.prole)
                        { if (A.x == x && A.y == y && (A.nome == puma)) { c = false; break; } }
                    }
                    break;
            }
            if (c==true)
            {
                Agente ag = new Agente() { s = pai.s, ale = pai.ale, x = x, y = y, agentes = pai.agentes, nome = pai.nome, col = pai.col, ext = pai.ext, my = pai.my, prole = pai.prole, rem=pai.rem };
                pai.prole.Add(ag);
            }
    }
}

    class Modelo
    {
        private int napresas = (int)((100-2)*(100-2)*0.4);                        //Número de agentes
        private int it = 6000;                              //Número de iterações
        private int Lx = 100;                               //Tamanho no eixo x
        private int Ly = 100;                               //Tamanho no eixo y
        private Random ale;                                 //Para gerar números aleatórios
        private List<Agente> Agentes = new List<Agente>();  //Lista de agentes
        private List<Agente> prole = new List<Agente>();    //lista de prole

        //Fracciones iniciales
        private double D   = 0.3;                          //fraccion inicial de sitios destruidos
        private double x10 = 0.5;                          //Probabilidade da presa ser x1
        private double y0 =  0.75;                          //Probabilidade de nascer um predador junto da presa    
        //A probabilidade de ser y é y0=1-x1-x2
        //Tasas               
        private double cx1  = 0.050;                          //colonizaciones       
        private double cx2  = 0.100; // cx2  >  cx1
        private double cy   = 0.015;
        private double ex1  = 0.050;                          //extinciones       
        private double ex2  = 0.010; // ex2  <  ex1
        private double ey   = 0.017; 
        private double mx1y = 0.200;                          //depredaciones       
        private double mx2y = 0.800; // mx2y >> mx1y
        //Garantir que os nomes das espécies estão corretos
        const string guanaco = "Guanaco";
        const string ovelha  = "Ovelha";
        const string puma    = "Puma";

        public Modelo() //Construto
        {
            ale = new Random();                         //Números aleatórios
 

            //Criar as presas
            for (int i = 0; i < napresas; i++)
            {


            Registro(Agentes,0);                                        //Registra
            for (int i = 0; i < it; i++)                                //Roda a simulação
            {
                Console.WriteLine(i);
                foreach (Agente A in Agentes)                           //Atualiza a lista de agentes vizinhos
                { A.Vizinhanca(); }
                foreach (Agente A in Agentes)                           //Faz cada agente colonizar
                { A.Colonizar(); }
                foreach (Agente A in Agentes)                           //Faz as pumas predarem
                { if (A.nome == puma) { A.Predar(); } }
                foreach (Agente A in Agentes)                           //Faz os guanacos causarem deslocamento
                { if (A.nome == guanaco) { A.Deslocamento(); } }
                foreach (Agente A in Agentes)                           //Causa a exxtinção de cada agente
                { A.Extincao(); }
                Agentes.RemoveAll((Agente obj) => obj.extinto == true);  //Removemos os agentes que foram predados
                Agentes.AddRange(prole);                                 //Adiciona a prole 
                prole.Clear();                                           //Zera a prole
                rem.Clear();
                Registro(Agentes,i+1);                                   //registra
            }
        }
        //Métodos auxiliares
        static void Registro(List<Agente> Agentes,int i)
        {
            //Guardar a quantidade de cada espécie
            int x1 = 0;
            int x2 = 0;
            int y  = 0;
            foreach (Agente A in Agentes)
            {
                x1 += (A.nome == guanaco) ? 1 : 0;
                x2 += (A.nome == ovelha ) ? 1 : 0;
                y  += (A.nome == puma   ) ? 1 : 0;
            }
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