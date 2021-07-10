/*
Exemplo de modelo baseado em indivíduos
Autor:           Jhordan Silveira de Borba
E-mail:          sbjhordan @gmail.com
Site:            https://sites.google.com/view/jdan/
Link:            http://www.geog.leeds.ac.uk/courses/other/crime/abm/general-modelling/index.html
*/

using System;               //Namespace padrão System
using System.Collections.Generic; //Para usar listas

namespace Vida_selvagem_e_Pecuária
{
    class Agente
    {
        public int ID;                                    //Identificação
        public int x = 5;                                 //Coordenadas espaciais
        public int y = 5;
        public int ouro = 0;                             //Dinheiro
        public string nome = "";                          //Que tipo de agente é
        public List<Agente> Agentes = new List<Agente>(); //Lista de todos os agentes
        public int[,] ambiente;                           //Configuraçõe do ambiente
        public int largura = 10;
        public int altura = 10;
        public bool serRemovido = false;                 //Se o a gente foi preso
        //Método para mover o agente
        public void Mover()
        {
            Random rnd = new Random();              //Gerador de número aleatório alimentado pelo sistema
            x += (rnd.NextDouble() < 0.5) ? -1 : 1; //Mover aleatoriamente para os lados
            y += (rnd.NextDouble() < 0.5) ? -1 : 1; //Mover aleatoriamente para cima e baixo
            //Obs.: Ele se move mais rápido na diagonal, pois o desloamento tem módulo maior que 1
            //Checar as fronteiras
            x = (x < 0) ? 0 : x;
            x = (x >= largura) ? largura - 1 : x;
            y = (y < 0) ? 0 : y;
            y = (y >= altura) ? altura - 1 : y;
        }
        //Método para roubar
        public void Agir()
        {
            if (serRemovido == true) { return; } //Se o agentee está sendo removido, nao faz nada
            if (nome == "ladrao")                //Interação com ambiente: se o agente atual é ladrão, checa a posição por ouro para roubar
            {
                if (ambiente[x, y] > 0)
                {
                    ouro += ambiente[x, y];
                    ambiente[x, y] = 0;
                }
            }
            foreach (Agente A in Agentes)       //Interação com outros agentes: 
            {
                if (A.ID == ID) { continue; }   //Se for o prórprio agente
                if ((A.x == x) && (A.y == y))
                {
                    if (A.nome == "ladrao")     //Se o outro agente não é policial, toma dinheiro dele
                    {
                        ouro = ouro + A.ouro;
                        A.ouro = 0;
                    }
                    //Se o atual agente é policial e o outro é ladrão, deve ser removido
                    A.serRemovido = (nome == "policial" && A.nome == "ladrao") ? true : false;
                }
            }
        }
        public void experimentar() //Função para testar algumas coisas em cada agente
        {
            serRemovido = true;
        }

    }

    class Modelo
    {
        private int nagentes = 100; //Número de agentes
        private int it = 100; // Número de iterações
        private double ppol = 0.1; //Probabilidade de ser gerado um poliial
        private double pbanco = 0.1; //Probabilidade de ser gerado um banco
        private int dbanco = 10;  //Dinheiro no banco
        private int largura = 100; //Largura do espaço
        private int altura = 100; //altura o espaço
        private int cont = 0;   //Contador de agentes
        List<Agente> Agentes = new List<Agente>();
        public Modelo() //Construto
        {
            Random rnd = new Random();                   //Números aleatórios
            int[,] ambiente = new int[largura, altura];  //Criar os bancos
            for (int i = 0; i < largura; i++)
            {
                for (int j = 0; j < altura; j++)
                {
                    ambiente[i, j] = (rnd.NextDouble() < pbanco) ? dbanco : 0; 
                }
            }
            for (int i = 0; i < nagentes; i++)              //Criar os agentes
            {
                Agente ag = new Agente() { ID = cont };
                cont += 1;
                ag.x = (int)(rnd.NextDouble() * largura);                  //Posição inicial aleatória
                ag.y = (int)(rnd.NextDouble() * altura);
                ag.ambiente = ambiente;                                    //Configura o ambiente
                ag.largura = largura;
                ag.altura = altura;
                ag.Agentes = Agentes;                                      //Conhece outros agentes
                ag.nome = (rnd.NextDouble() < ppol) ? "policial" : "ladrao"; //Policia ou Ladrão
                Agentes.Add(ag);                                           //Adiciona à lista
            }
            for (int i = 0; i < it; i++)                //Roda a simulação
            {
                Console.WriteLine(i);
                foreach (Agente A in Agentes)            //Move cada agente
                { A.Mover(); }
                foreach (Agente A in Agentes)
                { A.Agir(); }                            //Cada agente age
            }
            //Expressão lambda: um método anônimo. Exemplo:  x => x + 1, basicamente recebe x, e retorna x+1
            //Predicado: Recebe um parâmetro e retorna verdadeiro ou falso. Exemplo: Predicate<int> isOne = x => x == 1, recebe x e retorna verdadeiro se x==1
            Predicate<Agente> pred = (Agente obj) => obj.serRemovido == true; //Removemos os agentes fora do foreach, pra não acessar elemento que não existes
            Agentes.RemoveAll((Agente obj) => obj.serRemovido == true);
            //Estatísticas
            int cpol = 0;   //Quantos policiais tem
            int dpol = 0;   //Quanto dinheiro os policiais acumularam
            int clad = 0;   //Quantos ladroes tem
            int dlad = 0;   //Quanto dinheiro os ladrões acumularam
            foreach (Agente A in Agentes)
            {
            if (A.nome=="policial")
                {
                    cpol += 1;
                    dpol += A.ouro;
                }
            else
                {
                    clad += 1;
                    dlad += A.ouro;
                }
            }
            Console.WriteLine("Após " + it + " interações, há:");
            Console.WriteLine("- " + cpol + " policiais com " + dpol + " ouro.");
            Console.WriteLine("- " + clad + " ladroes com " + dlad + " ouro.");
        }
    }

    class Program
    {
        static void Main()
        {
            new Modelo();       //Inicia o modelo
            Console.ReadKey();
        }
    }
}