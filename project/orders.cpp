#include "orders.h"
#include <QFile>
#include <QJsonDocument>
#include <QJsonArray>
#include <QJsonObject>
#include <QDebug>
#include <QStandardPaths>
#include <QDir>

const QStringList names = {
    "Josef ", "Honza ", "Jiří ", "Tomáš ", "Petr ",
    "Martin ", "Janek ", "Lukáš ", "Michal ", "Jakub ",
    "David ", "Pavel ", "Jindřich ", "Adam ", "Marek ",
    "Václav ", "Filip ", "Ondřej ", "Dominik ", "Daniel ",
    "František ", "Miroslav ", "Richard ", "Zdeněk ", "Karel ",
    "Radek ", "Jaroslav ", "Aleš ", "Vojtěch ", "Robert ",
    "Patrik ", "Libor ", "Radim ", "Stanislav ", "Milan ",
    "René ", "Matěj ", "Radovan ", "Vladimír ", "Eldar ",
    "Šimon ", "Tadeáš ", "Bohumil ", "Bohuslav ", "Bořek ",
    "Bořivoj ", "Božek ", "Břetislav ", "Čeněk ", "Čestmír ",
    "Dalibor ", "Dobroslav ", "Dušan ", "Emil ", "Gabriel ",
    "Gustav ", "Hynek ", "Chval ", "Ignác ", "Ivo ",
    "Jáchym ", "Patrick ", "Janko ", "Gigli ", "Jeroným ",
    "Jonáš ", "Kamil ", "Kryštof ", "Lev ", "Matouš ",
    "Mikoláš ", "Nikolas ", "Oldřich ", "Olej ", "Oskar ",
    "Osmar ", "Otokar ", "Oto ", "Radan ", "Roman ",
    "Rostislav ", "Samuel ", "Silvestr ", "Soběslav ", "Abdullahi ",
    "Svatopluk ", "Štefan ", "Štěpán ", "Tomášek ", "Vasil ",
    "Viktor ", "Vilém ", "Vlastimil ", "Vladan ", "Zbyšek ",
    "Hans ", "Gandalf ", "Hugoslav ", "Batman ", "Superman "
};

const QStringList surnames = {
    "Letáček", "Blažek", "Frydrych", "Kpozo", "Ndefe",
    "Rusnák", "Buchta", "Veselý", "Klíma", "Tanko",
    "Pospíšil", "Marek", "Hájek", "Rigo", "Jelínek",
    "Malý", "Urban", "Richter", "Sýkora", "Kříž",
    "Adamec", "Vaněk", "Kratochvíl", "Zeman", "Šimek",
    "Beneš", "Holub", "Fišer", "Bartoš", "Vlček"
};

const QVector<QPair<QString, QString>> product_list = {
    {"Pizza Mozzarella", "179 Kč"},
    {"Pizza Quattro Formaggi", "179 Kč"},
    {"Pizza Vegetariano", "189 Kč"},
    {"Pizza Primavera", "189 Kč"}
};

const QStringList villages = {
    "Troubelice", "Lazce", "Dědinka", "Pískov", "Nová Hradečná",
    "Libina", "Červenka", "Lipinka", "Klopina", "Medlov",
    "Benkov", "Pňovice", "Střelice", "Mladeč", "Nové Zámky"
};


QVector<QVariantMap> loadOrders() {
    QVector<QVariantMap> orders;
    QString filePath = QDir::currentPath() + "/orders.json";

    QDir dir(QStandardPaths::writableLocation(QStandardPaths::AppDataLocation));
    if (!dir.exists()) {
        dir.mkpath(".");
    }

    QFile file(filePath);

    try {
        if (!file.exists()) {
            qDebug() << "File not found. Creating a new one at:" << filePath;
            if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
                file.write("[]");
                file.close();
            }
        }

        if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
            throw std::runtime_error("Unable to open file for reading.");
        }

        QByteArray jsonData = file.readAll();
        file.close();

        QJsonDocument doc = QJsonDocument::fromJson(jsonData);
        if (!doc.isArray()) {
            throw std::runtime_error("JSON data not in a list.");
        }

        QJsonArray jsonArray = doc.array();
        for (const QJsonValue &value : jsonArray) {
            if (value.isObject()) {
                orders.append(value.toObject().toVariantMap());
            }
        }
        qDebug() << "Loaded" << orders.size() << "orders from file.";

    } catch (const std::exception &e) {
        qWarning() << "Error loading JSON:" << e.what();
        return {};
    }

    return orders;
}


