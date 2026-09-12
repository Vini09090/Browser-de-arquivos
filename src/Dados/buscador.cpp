#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <filesystem>

#include "Files.h"

using namespace std;
namespace fs = std::filesystem;

vector<string> getBigrams(const string& str) {
    vector<string> pairs;
    string upperStr = str;

    transform(
        upperStr.begin(),
        upperStr.end(),
        upperStr.begin(),
        [](unsigned char c) {
            return static_cast<char>(toupper(c));
        }
    );

    if (upperStr.length() < 2) {
        return pairs;
    }

    for (size_t i = 0; i < upperStr.length() - 1; ++i) {
        pairs.push_back(upperStr.substr(i, 2));
    }

    return pairs;
}

double calculateSimilarity(const string& str1, const string& str2) {
    vector<string> pairs1 = getBigrams(str1);
    vector<string> pairs2 = getBigrams(str2);

    if (pairs1.empty() || pairs2.empty()) {
        return 0.0;
    }

    int intersection = 0;
    vector<string> pairs2Copy = pairs2;

    for (const auto& pair1 : pairs1) {
        for (size_t j = 0; j < pairs2Copy.size(); ++j) {
            if (pair1 == pairs2Copy[j]) {
                ++intersection;
                pairs2Copy.erase(pairs2Copy.begin() + j);
                break;
            }
        }
    }

    const size_t totalPairs = pairs1.size() + pairs2.size();

    if (totalPairs == 0) {
        return 0.0;
    }

    return (2.0 * intersection) / static_cast<double>(totalPairs);
}

struct ResultadoBusca {
    string caminho;
    string titulo;
    double similaridade;
};

int main(int argc, char* argv[]) {
    // O Python envia o termo como primeiro argumento.
    if (argc < 2) {
        return 1;
    }

    const string entrada = argv[1];

    if (entrada.empty()) {
        return 0;
    }

    // Evita caminho fixo sempre que possível:
    // o Python poderá alterar a raiz no futuro.
    const string raiz = "/home/vinicius";

    const vector<string> extensoes{
        ".pdf",
        ".epub",
        ".txt",
        ".doc",
        ".docx"
    };

    vector<string> arquivos = buscar_arquivos(raiz, extensoes);

    // 0.20 = 20%.
    const double LIMITE_SIMILARIDADE = 0.20;

    vector<ResultadoBusca> resultados;

    for (const string& arq : arquivos) {
        fs::path caminho(arq);

        // Compara com o nome, e não com o caminho completo.
        string nomeArquivo = caminho.stem().string();

        double similaridade =
            calculateSimilarity(entrada, nomeArquivo);

        if (similaridade >= LIMITE_SIMILARIDADE) {
            resultados.push_back({
                arq,
                nomeArquivo,
                similaridade
            });
        }
    }

    sort(
        resultados.begin(),
        resultados.end(),
        [](const ResultadoBusca& a, const ResultadoBusca& b) {
            return a.similaridade > b.similaridade;
        }
    );

    /*
        Comunicação C++ -> Python.

        Cada linha possui:
            similaridade|titulo|caminho

        Exemplo:
            1.000000|Dom Casmurro|/home/vinicius/Livros/Dom Casmurro.pdf
    */
    for (const auto& resultado : resultados) {
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
