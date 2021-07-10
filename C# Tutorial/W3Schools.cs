/*
Tutorial de C#
Autor:           Jhordan Silveira de Borba
E-mail:          sbjhordan @gmail.com
Site:            https://sites.google.com/view/jdan/
Link:            https://www.w3schools.com/cs/index.php
*/
using System;                                           //Nos permite usar as classes do namespace System

namespace Programa                                      //NAMESPACE: container para classes e outros namespaces, organizar o código
{
    class Classe                                        //CLASSE: Container para fields (dados, propriedades) e métodos (funções), é um construtor de objetos
    {
        public  string field   = "Field público";       //FIELD, PUBLIC: indica que pode ser acessado por todas classes
        private string privado = "Field privado";       //PRIVATE (padrão): indica que só pode ser acessado apenas pela própria classe
                                                        //Polimorfismo: os métodos da classe se sobrepõem aos dos filhos
        public virtual void Metodo()                    //METHOD, VOID: Não retorna nada, VIRTUAL: permite mudar a prioridade
        { Console.WriteLine(privado);}
        public Classe(string frase)                     //CONSTRUTOR, com o mesmo nome da classe, chamado quando o obejto é criado
        {Console.WriteLine("Esse objeto é " + frase);}
        public string propriedade1                      //PROPRIEDADE: Mistura de field e método
        {get { return privado;} set { privado = value;}}
        public string propriedade2 { get; set; }        //Versão resumida, não altera nenhuma variável
        public Classe()                                 //Um novo construto se quiser um filho sem herdar o construto
        { }
    }

    class Filho1 : Classe                                //Uma classe pode herdar outra
    {
        public Filho1(string frase) : base(frase)      //Herdar o constutor
        {}
        public override void Metodo()
        { Console.WriteLine("Sobrescreveu 1"); }
    }

    class Filho2 : Classe                                //Uma classe pode herdar outra
    {
        public Filho2(string frase)                      //Criando o construtor
        { Console.WriteLine("Filho " + frase); }
        public void Metodo()
        { Console.WriteLine("Sobrescreveu 2"); }
    }

    sealed class pai                                    //Protege contra herança
    {
        public pai()
        { Console.WriteLine("Child free"); }
    }

    abstract class PaiAbstrato   // CLASSE ABSTRATA: Não pode ser usada para criar objetos, para acessá-la é necessário usar herança
     {
        public abstract void Abstrata();  //MÉTODO ABSTRATO: Só pode ser usado em uma classe abstrata, não possui corpo, é herdado
        public PaiAbstrato()
        {Console.WriteLine("Classe Abastrata");}
     }

     class FilhoAbstrato : PaiAbstrato
      {
        public override void Abstrata()
         {Console.WriteLine("Metodo abstrato");}
        }

    interface Interface1 //Interface é uma classe totalmente abstrata, não pode possuir fields e métodos e propriedades devem estar vazios
    {void MetInter1();}//Não pode ter construtor, e precisa 'sofrer override'
    interface Interface2 //pode possuir duas interfaces
    { void MetInter2(); }

    class FilhoInter : Interface1, Interface2
    {
        public void MetInter1()
        {Console.WriteLine("Pai 1");}
        public void MetInter2()
        { Console.WriteLine("Pai 2"); }
    }

    enum Constantes //Classe de constantes
    {
        Baixo,    // 0
        Medio=3,  // 3
        Alto      // 4   
    }

    class Principal
    {
        string field = "Field local";
        static void Main(string[] args)                     // STATIC: significa que pode ser acessado sem crar um objeto da classe
        { 
            //Namespace System contém uma classe Console com o método WriteLine()
            Console.WriteLine("Hello World!");
            Classe Obj = new Classe("Porreta");             //Criamos um obeto "myObj" da classe carro
            Console.WriteLine(Obj.field);                   //Acessamos um field
            Obj.Metodo();                                   //E aessamos o método 
            Obj.propriedade1 = "Mudou o field privado";     //Usa o set na propriedade
            Console.WriteLine(Obj.propriedade1);            //Usa o get na propriedade
            Obj.Metodo();
            Console.WriteLine(Obj.propriedade2);
            Obj.propriedade2 = "Viva a propriedade alternativa!";
            Console.WriteLine(Obj.propriedade2);
            Principal Obj2 = new Principal();               //Pode-se definir um objeto dentro da própria função
            Console.WriteLine(Obj2.field);
            Classe Obj3 = new Filho1("filho");             
            Classe Obj4 = new Filho2("rebelde");
            pai Obj5 = new pai();
            Obj.Metodo();
            Obj3.Metodo();
            Obj4.Metodo();
            FilhoAbstrato Obj6 = new FilhoAbstrato();
            Obj6.Abstrata();
            FilhoInter Obj7 = new FilhoInter();
            Obj7.MetInter1();
            Obj7.MetInter2();
            Console.WriteLine(Constantes.Alto);
            int CC = (int)Constantes.Alto;
            Console.WriteLine(CC);
            Console.ReadKey();

        }
    }
}

// Conclusão: Herança é algo que precisa ser melhor estudado para saber o que está acontecendo exatamente. Por exemplo a diferença de definir dois objetos:
// Pai Objeto = new Filho()
// Filho Objeto = new Filho()