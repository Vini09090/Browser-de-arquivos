// Exemplo 1 - usando vetor em C++
// Vetor de inteiros imprimido na saida do programa
#include <iostream>
#include <vector>
#include <filesystem>


//Criasse para comparar strings recebidas e localizadas, e retornar os resultados nos quais, eu possuo uma boa margem de acerto? 
//Assim eu teria necessariamente uma boa forma de filtragem pois assim, eu conseguiria limitar os erros de escrita.
using namespace std;
namespace fs = std::filesystem;
const string raiz = "/home/vinicius";


std::vector<std::string> buscar_arquivos(
    const std::string& caminho,
    const std::vector<std::string>& extensoes
) {
    std::vector<std::string> resultado;

    for (const auto& entry :
         fs::recursive_directory_iterator(caminho)) {

        if (!entry.is_regular_file())
            continue;

        std::string extensao = entry.path().extension().string();

        for (const std::string& permitida : extensoes) {
            if (extensao == permitida) {
                resultado.push_back(entry.path().string());
                break;
            }
        }
    }

    return resultado;
}
std::vector<std::string> filtro(
    std::string nome,
    const std::vector<std::string>& extensoes
) {
    std::vector<std::string> arquivos =
        buscar_arquivos(raiz, extensoes);

    std::vector<std::string> resultado;

    for (const std::string& arquivo : arquivos) {

        if (arquivo.find(nome) != std::string::npos) {
            resultado.push_back(arquivo);
        }

    }

    return resultado;
}

int main() {

    std::vector<std::string> extensoes{
        ".pdf",
        ".txt",
        ".doc",
        ".docx"
    };

    std::vector<std::string> resultados =
        filtro("Cal", extensoes);

    for (const std::string& arquivo : resultados) {
        std::cout << arquivo << std::endl;
    }

    return 0;
}