#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <filesystem>

#include "Files.h"

using namespace std;
namespace fs = std::filesystem;

vector<string> getBigrams(const string& str)
{
    vector<string> pairs;

    string texto = str;

    transform(
        texto.begin(),
        texto.end(),
        texto.begin(),
        [](unsigned char c)
        {
            return static_cast<char>(toupper(c));
        }
    );

    if (texto.length() < 2)
    {
        return pairs;
    }

    for (size_t i = 0; i < texto.length() - 1; ++i)
    {
        pairs.push_back(
            texto.substr(i, 2)
        );
    }

    return pairs;
}

// Retorno:
// 0.0 = 0%
// 0.5 = 50%
// 1.0 = 100%


double calculateSimilarity(
    const string& str1,
    const string& str2
)
{
    vector<string> pairs1 =
        getBigrams(str1);

    vector<string> pairs2 =
        getBigrams(str2);

    if (
        pairs1.empty() ||
        pairs2.empty()
    )
    {
        return 0.0;
    }

    int intersection = 0;

    vector<string> copia = pairs2;

    for (const string& pair1 : pairs1)
    {
        for (size_t j = 0; j < copia.size(); ++j)
        {
            if (pair1 == copia[j])
            {
                ++intersection;

                copia.erase(
                    copia.begin() + j
                );

                break;
            }
        }
    }

    int total =
        pairs1.size() +
        pairs2.size();

    if (total == 0)
    {
        return 0.0;
    }

    return (
        2.0 *
        intersection
    ) / total;
}

// Estrutura dos resultados


struct ResultadoBusca
{
    string titulo;
    string caminho;
    double similaridade;
};



// Programa principal


int main(int argc, char* argv[])
{
    // --------------------------------------------------------
    // O Python precisa enviar o termo da pesquisa
    // --------------------------------------------------------

    if (argc < 2)
    {
        return 1;
    }

    string entrada = argv[1];

    if (entrada.empty())
    {
        return 0;
    }




    const string raiz =
        "/home/vinicius";



    vector<string> extensoes
    {
        ".pdf",
        ".epub",
        ".txt",
        ".doc",
        ".docx"
    };

    // Busca os arquivos usando Files.h
 

    vector<string> arquivos =
        buscar_arquivos(
            raiz,
            extensoes
        );

    // Limite mínimo
    //
    // 0.20 = 20%


    const double LIMITE =
        0.20;

    vector<ResultadoBusca> resultados;


    for (const string& arquivo : arquivos)
    {
        fs::path caminho(arquivo);


        // Nome sem extensão
        string nome =
            caminho.stem().string();


        // Calcula a similaridade
        double similaridade =
            calculateSimilarity(
                entrada,
                nome
            );


        if (similaridade >= LIMITE)
        {
            resultados.push_back(
                {
                    nome,
                    arquivo,
                    similaridade
                }
            );
        }
    }


    sort(
        resultados.begin(),
        resultados.end(),
        [](const ResultadoBusca& a,
           const ResultadoBusca& b)
        {
            return
                a.similaridade >
                b.similaridade;
        }
    );


    for (
        const auto& resultado :
        resultados
    )
    {
        cout
            << resultado.similaridade
            << "|"
            << resultado.titulo
            << "|"
            << resultado.caminho
            << '\n';
    }


    return 0;
}
