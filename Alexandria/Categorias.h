#ifndef CATEGORIAS_H
#define CATEGORIAS_H

#include <iostream>
#include <vector>
#include <string>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

//Cria as subpastas na pasta Biblioteca

vector<string> agrupamento(const vector<string>& grupos, const fs::path& pastaPai) {

    try {
        if (!fs::exists(pastaPai)) {
            fs::create_directories(pastaPai);
            cout << "Pasta biblioteca criada: " << pastaPai << endl;
        }
    }
    catch (const fs::filesystem_error& e) {
        cerr << "Erro ao criar a pasta biblioteca: " << e.what() << endl;
        return {};
    }

    for (const string& categoria : grupos) {

        fs::path caminhoSubpasta = pastaPai / categoria;

        try {
            if (!fs::exists(caminhoSubpasta)) {
                fs::create_directories(caminhoSubpasta);
                cout << "Pasta criada: " << caminhoSubpasta << endl;
            }
            else {
                cout << "Pasta ja existe: " << caminhoSubpasta << endl;
            }
        }
        catch (const fs::filesystem_error& e) {
            cerr << "Erro ao criar a categoria "
                 << categoria << ": "
                 << e.what() << endl;
        }
    }

    return grupos;
}

#endif
