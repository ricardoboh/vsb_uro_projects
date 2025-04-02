#include <QApplication>
#include <QDebug>
#include "mainwindow.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    // Create and show the main window
    MainWindow mainWindow;
    mainWindow.setWindowTitle("Pizzeria Application");
    mainWindow.showMaximized();
    mainWindow.show();

    return app.exec();
}
