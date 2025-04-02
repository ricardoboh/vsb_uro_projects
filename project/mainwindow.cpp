#include "mainwindow.h"
#include "orders.h"

#include <QApplication>
#include <QScreen>
#include <QFile>
#include <QJsonDocument>
#include <QJsonArray>
#include <QJsonObject>
#include <QDateTime>
#include <QRandomGenerator>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QTabWidget>
#include <QScrollArea>
#include <QMessageBox>
#include <QShortcut>
#include <QKeyEvent>
#include <QMenu>
#include <QAction>
#include <QWheelEvent>
#include <QScrollBar>
#include <QDialog>
#include <QSpacerItem>
#include <QVariantMap>
#include <QMap>
#include <QDebug>
#include <QStandardPaths>
#include <QRegularExpression>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    varTakeAwaySum = 0;
    varDeferment = 0;
    varCash = 0;
    varFinalSum = 0;
    varDailyPrice = 0;
    varOrderNum = 0;
    varDateFirstOrder = "";
    varDateLastOrder = "";
    varActualDate = "";

    for (int i = 1; i <= 6; ++i) {
        varDictDeliveries[i] = 0;
    }

    centralWidget = new QWidget(this);
    setCentralWidget(centralWidget);
    mainLayout = new QVBoxLayout(centralWidget);

    createMainPageLayout();
    createNotebook();
}


MainWindow::~MainWindow()
{
}

void MainWindow::createMainPageLayout()
{
    headerFrame = new QWidget(this);
    headerFrame->setStyleSheet(QString("background-color: %1; height: 40px;")
                                   .arg(background_color_secondary));

    mainFrame = new QWidget(this);
    mainFrame->setStyleSheet(QString("background-color: %1;")
                                 .arg(background_color_primary));

    createHeaderLayout();

    mainLayout->addWidget(headerFrame);
    mainLayout->addWidget(mainFrame);
}

void MainWindow::createHeaderLayout()
{
    headerLayout = new QHBoxLayout(headerFrame);
    headerLayout->setContentsMargins(0, 0, 0, 0);

    lblBranchName = new QLabel("Bistro Olomouc - BOH0162", headerFrame);
    lblBranchName->setStyleSheet("color: white; margin-left: 25; font-size: 20px; font-weight: bold;");

    btnCreateOrder = new QPushButton("VYTVOŘIT OBJEDNÁVKU", headerFrame);
    btnCreateOrder->setStyleSheet(QString("background-color: %1; width: 350px; font-size: 20px;")
                                      .arg(darker_blue));
    connect(btnCreateOrder, &QPushButton::clicked, this, &MainWindow::generateRandomOrder);

    btnLogout = new QPushButton("Odhlasit se", headerFrame);
    btnLogout->setStyleSheet(QString("color: white; background-color: %1; border: none; margin-right: 40px;"
                                     "font-size: 18px; font-weight: bold;")
                                 .arg(background_color_secondary));
    connect(btnLogout, &QPushButton::clicked, this, &MainWindow::logout);


    headerLayout->addWidget(lblBranchName);
    headerLayout->addStretch();
    headerLayout->addWidget(btnCreateOrder);
    headerLayout->addStretch();
    headerLayout->addWidget(btnLogout);
}



void MainWindow::createNotebook()
{
    notebook = new QTabWidget(mainFrame);
    notebook->setStyleSheet("QTabWidget::pane { margin: 0; padding: 0; }");

    frameActiveOrders = new QWidget();
    frameHistoryOrders = new QWidget();
    frameShiftEnd = new QWidget();

    shiftEndLayout = new QVBoxLayout(frameShiftEnd);
    activeOrdersLayout = new QVBoxLayout(frameActiveOrders);
    historyOrdersLayout = new QVBoxLayout(frameHistoryOrders);

    createShiftEndPage();
    createHistoryOrdersPage();
    createActiveOrdersPage();

    notebook->addTab(frameActiveOrders, "Aktivní objednávky");
    notebook->addTab(frameHistoryOrders, "Historie objednávek");
    notebook->addTab(frameShiftEnd, "Konec směny");

    connect(notebook, &QTabWidget::currentChanged, this, &MainWindow::onTabSelected);
    mainLayout->addWidget(notebook);

    floatingButton = new QPushButton("+", notebook);
    floatingButton->setStyleSheet(QString("font: bold 56px Helvetica; background-color: %1; color: white;"
                                          "border-radius: 60px; padding: 10px;")
                                      .arg(light_blue));
    floatingButton->setFixedSize(120, 120);
    connect(floatingButton, &QPushButton::clicked, this, &MainWindow::generateRandomOrder);
    floatingButton->move(notebook->width() - floatingButton->width() - 20,
                         notebook->height() - floatingButton->height() - 20);
    floatingButton->raise();
    connect(floatingButton, &QPushButton::clicked, this, []() {
    });
    connect(notebook, &QTabWidget::currentChanged, this, [=]() {
        floatingButton->raise();
    });
}

void MainWindow::resizeEvent(QResizeEvent *event)
{
    QMainWindow::resizeEvent(event);
    if (floatingButton && notebook) {
        floatingButton->move(notebook->width() - floatingButton->width() - 20,
                             notebook->height() - floatingButton->height() - 20);
        floatingButton->raise();
    }
}



void MainWindow::logout()
{
    QMessageBox::information(this, "Logout", "Odhlásili jste se.");
}



void MainWindow::onTabSelected(int index)
{
    QString tabText = notebook->tabText(index);

    if (tabText == "Konec směny") {
        QString currentDateTime = QDateTime::currentDateTime().toString("dd.MM.yyyy hh:mm:ss");
        valueGenerated->setText(currentDateTime);
    }
}


void MainWindow::createShiftEndInfo()
{
    frameGenerated = new QWidget(frameEndInfoShiftEnd);
    QVBoxLayout *frameLayout = new QVBoxLayout(frameGenerated);
    frameLayout->setContentsMargins(5, 5, 5, 5);
    frameLayout->setAlignment(Qt::AlignTop | Qt::AlignLeft);

    lblEnd = new QLabel("UZÁVĚRKA FINANCÍ SMĚNY", frameGenerated);
    lblEnd->setStyleSheet("font: bold 18px Helvetica;");
    lblEnd->setAlignment(Qt::AlignLeft);
    frameLayout->addWidget(lblEnd);

    QGridLayout *shiftEndGridLayout = new QGridLayout();
    shiftEndGridLayout->setSpacing(15);
    shiftEndGridLayout->setContentsMargins(0, 0, 0, 20);


    auto addInfoRow = [&](int row, const QString &labelText, QLabel *&valueLabel) {
        QLabel *label = new QLabel(labelText, frameGenerated);
        label->setStyleSheet("font: 18px Helvetica;");
        label->setFixedWidth(260);

        valueLabel = new QLabel("---", frameGenerated);
        valueLabel->setStyleSheet("font: 18px Helvetica; color: white;");
        valueLabel->setAlignment(Qt::AlignLeft);

        shiftEndGridLayout->addWidget(label, row, 0);
        shiftEndGridLayout->addWidget(valueLabel, row, 1);
    };


    addInfoRow(0, "Uzávěrka generována:", valueGenerated);
    addInfoRow(1, "První objednávka přijata:", valueDateFrom);
    addInfoRow(2, "Poslední objednávka přijata:", valueDateTo);
    addInfoRow(3, "Počet objednávek:", valueNumOfOrders);

    frameLayout->addLayout(shiftEndGridLayout);

    frameDeliveries = new QWidget(frameGenerated);
    QVBoxLayout *deliveriesLayout = new QVBoxLayout(frameDeliveries);
    deliveriesLayout->setContentsMargins(10, 0, 0, 20);

    lblAllDeliveriesInfo = new QLabel("Rozdělení podle rozvozců:", frameGenerated);
    lblAllDeliveriesInfo->setStyleSheet("font: bold 16px Helvetica;");
    deliveriesLayout->addWidget(lblAllDeliveriesInfo);
    frameDeliveries->setLayout(deliveriesLayout);
    frameLayout->addWidget(frameDeliveries);

    QGridLayout *summaryGridLayout = new QGridLayout();
    summaryGridLayout->setSpacing(5);
    summaryGridLayout->setContentsMargins(0, 0, 0, 0);

    auto addSummaryRow = [&](int row, const QString &labelText, QLabel *&valueLabel) {
        QLabel *label = new QLabel(labelText, frameGenerated);
        label->setStyleSheet("font: bold 16px Helvetica;");
        label->setFixedWidth(180);

        valueLabel = new QLabel("---", frameGenerated);
        valueLabel->setStyleSheet("font: bold 16px Helvetica; color: #2958cf;");
        valueLabel->setAlignment(Qt::AlignLeft);

        summaryGridLayout->addWidget(label, row, 0);
        summaryGridLayout->addWidget(valueLabel, row, 1);
    };

    addSummaryRow(0, "CELKEM HOTOVO:", valueSumDone);
    addSummaryRow(1, "Přijato celkem:", valueSumAll);
    frameLayout->addLayout(summaryGridLayout);
    frameGenerated->setLayout(frameLayout);

    QVBoxLayout *infoLayout = qobject_cast<QVBoxLayout*>(frameEndInfoShiftEnd->layout());
    if (!infoLayout) {
        infoLayout = new QVBoxLayout(frameEndInfoShiftEnd);
        infoLayout->setAlignment(Qt::AlignTop | Qt::AlignLeft);
        frameEndInfoShiftEnd->setLayout(infoLayout);
    }
    infoLayout->addWidget(frameGenerated);
}



void MainWindow::uploadInvoice()
{
    QString filename = QFileDialog::getOpenFileName(this, "Vyberte soubor", "", "All Files (*.*)");
    if (!filename.isEmpty()) {
        qDebug() << "Vybráno:" << filename;
    } else {
        qDebug() << "Žádný soubor nebyl vybrán.";
    }
}

void MainWindow::printOrder()
{
    QMessageBox::information(this, "Tisk Objednávky", "Tisk probíhá odsouhlaste tlačítkem");
}


void MainWindow::countEndShift()
{
    if (!errorLabel) {
        errorLabel = new QLabel(frameErrorLabel);
        errorLabel->setText("");
        errorLabel->setStyleSheet(errorLabelText);
        errorLabel->setAlignment(Qt::AlignTop | Qt::AlignLeft);
        errorLabel->setWordWrap(true);
        errorLabel->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::MinimumExpanding);
        errorLabel->setFixedWidth(390);
        errorLabel->setFixedHeight(500);
    }

    if (!btnSaveEndShift) {
        btnSaveEndShift = new QPushButton("Uložit konec směny", this);
        btnSaveEndShift->setStyleSheet(btnBackground);
        btnSaveEndShift->setEnabled(false);
    }

    if (entryFields.isEmpty()) {
        entryFields["oSum"] = new QLineEdit(this);
        entryFields["cSum"] = new QLineEdit(this);
        entryFields["fSum"] = new QLineEdit(this);
        entryFields["sSum"] = new QLineEdit(this);
        entryFields["cash"] = new QLineEdit(this);
        entryFields["deferment"] = new QLineEdit(this);

        for (auto &entry : entryFields) {
            entry->setPlaceholderText("0");
            entry->setText("0");
            entry->setStyleSheet(enabledStyle);
            entry->setParent(this);

            connect(entry, &QLineEdit::textChanged, this, [=]() {
                countEndShift();
            });
        }
    }

    bool errorFound = false;

    for (auto key : entryFields.keys()) {
        bool ok;
        QString textValue = entryFields[key]->text();

        if (textValue.trimmed().isEmpty()) {
            textValue = "0";
            entryFields[key]->setText(textValue);
        }

        int value = textValue.toInt(&ok);

        if (ok) {
            entryFields[key]->setStyleSheet(validStyle);
            values[key] = value;
        } else {
            entryFields[key]->setStyleSheet(invalidStyle);
            errorFound = true;
        }

        if (entryFields[key]->isEnabled()) {
            entryFields[key]->setStyleSheet(enabledStyle);
        } else {
            entryFields[key]->setStyleSheet(disabledStyle);
        }
    }

    if (errorFound) {
        showErrorMessage("V poli s červeným pozadím\n"
                         "je jiný znak, než číslo.\n"
                         "Prosím pište jen čísla.\n");
    } else {
        makeFinalSum();
    }
}




void MainWindow::makeFinalSum()
{
    int expenses = values["cSum"] + values["fSum"] + values["sSum"];

    if (values["oSum"] < expenses) {
        bool errorField = false;
        for (const QString &key : {"cSum", "fSum", "sSum"}) {
            if (values[key] > values["oSum"]) {
                entryFields[key]->setStyleSheet(invalidStyle);
                errorField = true;
            } else {
                entryFields[key]->setStyleSheet(enabledStyle);
            }
        }

        if (errorField) {
            showErrorMessage("Pole s červeným pozadím má neočekávaně vysokou hodnotu.\nProsím zkontrolujte toto pole.");
        } else {
            showErrorMessage("Celkové výdaje jsou vyšší, než by se očekávalo.\nPokud se dělal velký nákup, předložte účtenku.");
        }
    } else {
        int sumWithDeferment = values["oSum"] - expenses;

        if (sumWithDeferment < 1000) {
            varDeferment = sumWithDeferment;
            varCash = 0;
        } else {
            varDeferment = 1000;
            varCash = sumWithDeferment - 1000;
        }

        entryFields["deferment"]->setText(QString::number(varDeferment));
        entryFields["cash"]->setText(QString::number(varCash));

        showSuccessMessage();
        btnSaveEndShift->setEnabled(true);
    }
}


void MainWindow::showErrorMessage(const QString &message)
{
    if (!errorLabel) {
        errorLabel = new QLabel(frameErrorLabel);
        errorLabel->setStyleSheet("font: 16pt 'Helvetica'; color: black; background-color: lightgrey;"
                                  "padding-top: 30px; padding-left: 10px;");
        errorLabel->setAlignment(Qt::AlignTop | Qt::AlignLeft);
        errorLabel->setWordWrap(true);
        errorLabel->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::MinimumExpanding);
        errorLabel->setFixedWidth(390);
        errorLabel->setFixedHeight(500);
    }
    errorLabel->setText(message);
    errorLabel->setStyleSheet("font: 16pt 'Helvetica'; color: white; background-color: lightcoral;"
                              "padding-top: 30px; padding-left: 10px;");
}

void MainWindow::showSuccessMessage()
{
    if (!errorLabel) {
        errorLabel = new QLabel(frameErrorLabel);
        errorLabel->setText("");
        errorLabel->setStyleSheet("font: 16pt 'Helvetica'; color: black; background-color: lightgrey;"
                                  "padding-top: 30px; padding-left: 10px;");
        errorLabel->setAlignment(Qt::AlignTop | Qt::AlignLeft);
        errorLabel->setWordWrap(true);
        errorLabel->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::MinimumExpanding);
        errorLabel->setFixedWidth(390);
        errorLabel->setFixedHeight(500);
    }

    QString successMessage;
    if (varCash == 0 && entryFields["cSum"]->text() == "0" && entryFields["fSum"]->text() == "0") {
        successMessage = "\nDo obálky neodevzdáváte žádnou hotovost, stravenkové karty ani účtenky z karet.";
    } else {
        successMessage = "Vše vypadá dobře spočítáno.\nDo obálky prosím odevzdejte:\n";

        if (varCash != 0) {
            successMessage += QString("\t%1 Kč v hotovosti\n").arg(varCash);
        }
        if (entryFields["cSum"]->text() != "0") {
            successMessage += QString("\t%1 Kč v účtenkách karet\n").arg(entryFields["cSum"]->text().toInt());
        }
        if (entryFields["fSum"]->text() != "0") {
            successMessage += QString("\t%1 Kč ve stravenkách\n").arg(entryFields["fSum"]->text().toInt());
        }
    }

    errorLabel->setText(successMessage);
    errorLabel->setStyleSheet("font: 16pt 'Helvetica'; background-color: lightgreen; color: black;"
                              "padding-top: 30px; padding-left: 10px;");
}



void MainWindow::EditEndShiftForm()
{
    btnCountEndShift->setText("KONTROLA");
    connect(btnCountEndShift, &QPushButton::clicked, this, &MainWindow::countEndShift);

    QString enabledStyle = "font: 16pt 'Helvetica'; color: black; background-color: white;";

    entryFields["cSum"]->setEnabled(true);
    entryFields["cSum"]->setStyleSheet(enabledStyle);

    entryFields["fSum"]->setEnabled(true);
    entryFields["fSum"]->setStyleSheet(enabledStyle);

    entryFields["sSum"]->setEnabled(true);
    entryFields["sSum"]->setStyleSheet(enabledStyle);

    entryFields["oSum"]->setEnabled(true);
    entryFields["oSum"]->setStyleSheet(enabledStyle);

    entryFields["cash"]->setEnabled(true);
    entryFields["cash"]->setStyleSheet(enabledStyle);
}

void MainWindow::SaveEndShift()
{
    btnCountEndShift->setText("UPRAVIT");
    connect(btnCountEndShift, &QPushButton::clicked, this, &MainWindow::EditEndShiftForm);

    QString disabledStyle = "font: 16pt 'Helvetica'; color: white; background-color: #A9A9A9;";

    entryFields["cSum"]->setEnabled(false);
    entryFields["cSum"]->setStyleSheet(disabledStyle);

    entryFields["fSum"]->setEnabled(false);
    entryFields["fSum"]->setStyleSheet(disabledStyle);

    entryFields["sSum"]->setEnabled(false);
    entryFields["sSum"]->setStyleSheet(disabledStyle);

    entryFields["oSum"]->setEnabled(false);
    entryFields["oSum"]->setStyleSheet(disabledStyle);

    entryFields["cash"]->setEnabled(false);
    entryFields["cash"]->setStyleSheet(disabledStyle);
}





void MainWindow::CreateForm()
{
    if (!frameEndFormShiftEnd) {
        return;
    }

    QVBoxLayout *formLayout = qobject_cast<QVBoxLayout*>(frameEndFormShiftEnd->layout());
    if (!formLayout) {
        formLayout = new QVBoxLayout(frameEndFormShiftEnd);
        formLayout->setAlignment(Qt::AlignTop);
        formLayout->setContentsMargins(10, 10, 10, 10);
        frameEndFormShiftEnd->setLayout(formLayout);
    }

    frameEndFormShiftEnd->setFixedWidth(550);

    struct FormField {
        QString label;
        QString key;
        bool isEditable;
        int* variable;
    };

    QVector<FormField> fields = {
        {"Objednávky bistro:", "oSum", true, &varTakeAwaySum},
        {"Zaplaceno stravenkami:", "fSum", true, &varFoodCarts},
        {"Zaplaceno kartou:", "cSum", true, &varCards},
        {"Výdaje navíc:", "sSum", true, &varShopping},
        {"Denní odklad (1000Kč):", "deferment", false, &varDeferment},
        {"Odevzdat v hotovosti:", "cash", false, &varCash}
    };

    int row = 1;
    for (const auto &field : fields) {
        QLabel *label = new QLabel(field.label, frameEndFormShiftEnd);
        label->setStyleSheet("font: 16pt 'Helvetica'; margin: 5px 0;");
        labelFields[field.key] = label;

        QLineEdit *entry = new QLineEdit(frameEndFormShiftEnd);
        entry->setPlaceholderText("0");
        entry->setStyleSheet(field.isEditable ? enabledStyle : disabledStyle);
        entry->setEnabled(field.isEditable);
        entry->setFixedHeight(35);
        entry->setFixedWidth(180);
        entryFields[field.key] = entry;

        if (field.variable) {
            connect(entry, &QLineEdit::textChanged, this, [=]() {
                // https://stackoverflow.com/questions/70865734/qregexp-no-such-file-or-direcory
                QRegularExpression regExp("^[0-9]*$");
                QRegularExpressionMatch match = regExp.match(entry->text());
                if (match.hasMatch()) {
                    int value = entry->text().toInt();
                    *(field.variable) = value;
                    entry->setStyleSheet(enabledStyle);
                    errorLabel->setText("");
                    errorLabel->setStyleSheet("font: 16pt 'Helvetica'; color: black; background-color: lightgrey;"
                                              "padding-top: 30px; padding-left: 10px;");
                } else {
                    *(field.variable) = 0;
                    entry->setStyleSheet(invalidStyle);
                    showErrorMessage("V poli s červeným pozadím\n"
                                     "je jiný znak, než číslo.\n"
                                     "Prosím pište jen čísla.\n");
                }

                errorLabel->setText("");
                errorLabel->setStyleSheet("font: 16pt 'Helvetica'; background-color: lightgrey; color: black;"
                                          "padding-top: 30px; padding-left: 10px;");
                btnSaveEndShift->setEnabled(false);
            });
        } else {
            connect(entry, &QLineEdit::textChanged, this, [=]() {
                errorLabel->setText("");
                errorLabel->setStyleSheet("font: 16pt 'Helvetica'; background-color: lightgrey; color: black;"
                                          "padding-top: 30px; padding-left: 10px;");
                btnSaveEndShift->setEnabled(false);
            });
        }


        QHBoxLayout *rowLayout = new QHBoxLayout();
        rowLayout->setSpacing(5);
        rowLayout->addWidget(label);
        rowLayout->addWidget(entry);
        rowLayout->setAlignment(Qt::AlignLeft);

        QWidget *rowWidget = new QWidget(frameEndFormShiftEnd);
        rowWidget->setLayout(rowLayout);

        formLayout->addWidget(rowWidget);
        row++;
    }

    QWidget *buttonsFrame = new QWidget(frameEndFormShiftEnd);
    QHBoxLayout *buttonsLayout = new QHBoxLayout(buttonsFrame);
    buttonsLayout->setSpacing(40);
    buttonsLayout->setAlignment(Qt::AlignRight);

    btnSaveEndShift = new QPushButton("ULOŽIT", buttonsFrame);
    btnSaveEndShift->setStyleSheet("font: 16pt 'Helvetica'; padding: 8px;");
    btnSaveEndShift->setFixedWidth(140);
    btnSaveEndShift->setEnabled(false);
    connect(btnSaveEndShift, &QPushButton::clicked, this, &MainWindow::SaveEndShift);
    buttonsLayout->addWidget(btnSaveEndShift);

    btnCountEndShift = new QPushButton("KONTROLA", buttonsFrame);
    btnCountEndShift->setStyleSheet("font: 16pt 'Helvetica'; padding: 8px;");
    btnCountEndShift->setFixedWidth(186);
    connect(btnCountEndShift, &QPushButton::clicked, this, &MainWindow::countEndShift);
    buttonsLayout->addWidget(btnCountEndShift);

    formLayout->addWidget(buttonsFrame);
    frameEndFormShiftEnd->setLayout(formLayout);
}


void MainWindow::createShiftEndPage()
{
    QVBoxLayout *shiftEndLayout = qobject_cast<QVBoxLayout*>(frameShiftEnd->layout());
    if (!shiftEndLayout) {
        shiftEndLayout = new QVBoxLayout(frameShiftEnd);
        shiftEndLayout->setAlignment(Qt::AlignTop);
        frameShiftEnd->setLayout(shiftEndLayout);
    }

    frameInteractiveShiftEnd = new QWidget(frameShiftEnd);
    QVBoxLayout *interactiveLayout = new QVBoxLayout(frameInteractiveShiftEnd);
    interactiveLayout->setAlignment(Qt::AlignTop);

    frameButtonsShiftEnd = new QWidget(frameInteractiveShiftEnd);
    QHBoxLayout *buttonsLayout = new QHBoxLayout(frameButtonsShiftEnd);
    buttonsLayout->setAlignment(Qt::AlignTop);

    btnPrintEnd = new QPushButton("TISK DENNÍ UZÁVĚRKY", frameButtonsShiftEnd);
    btnPrintEnd->setStyleSheet("background-color: #97c2f7; color: black; font: 17px");
    btnPrintEnd->setFixedWidth(240);
    btnPrintEnd->setFixedHeight(40);
    connect(btnPrintEnd, &QPushButton::clicked, this, &MainWindow::printEndShift);
    buttonsLayout->addWidget(btnPrintEnd);

    btnSaveInvoice = new QPushButton("NAHRÁT FAKTURU/ÚČTENKU", frameButtonsShiftEnd);
    btnSaveInvoice->setStyleSheet("background-color: #97c2f7; color: black; font: 17px");
    btnSaveInvoice->setFixedWidth(240);
    btnSaveInvoice->setFixedHeight(40);
    connect(btnSaveInvoice, &QPushButton::clicked, this, &MainWindow::uploadInvoice);
    buttonsLayout->addWidget(btnSaveInvoice);

    frameButtonsShiftEnd->setLayout(buttonsLayout);
    interactiveLayout->addWidget(frameButtonsShiftEnd);

    QHBoxLayout *infoFormErrorLayout = new QHBoxLayout();
    infoFormErrorLayout->setAlignment(Qt::AlignTop);

    frameEndInfoShiftEnd = new QWidget(frameInteractiveShiftEnd);
    infoFormErrorLayout->addWidget(frameEndInfoShiftEnd);

    frameEndFormShiftEnd = new QWidget(frameInteractiveShiftEnd);
    QVBoxLayout *formFrameLayout = new QVBoxLayout(frameEndFormShiftEnd);
    formFrameLayout->setAlignment(Qt::AlignTop);
    frameEndFormShiftEnd->setLayout(formFrameLayout);
    infoFormErrorLayout->addWidget(frameEndFormShiftEnd);

    frameErrorLabel = new QWidget(frameInteractiveShiftEnd);
    QVBoxLayout *errorLayout = new QVBoxLayout(frameErrorLabel);
    errorLayout->setAlignment(Qt::AlignTop);

    errorLabel = new QLabel("Vyplňte formulář \nzkontrolujte zadané údaje", frameErrorLabel);
    errorLabel->setStyleSheet("font: 16pt 'Helvetica'; color: black; background-color: lightgrey;"
                              "padding-top: 30px; padding-left: 10px;");
    errorLabel->setAlignment(Qt::AlignTop | Qt::AlignLeft);
    errorLabel->setWordWrap(true);
    errorLabel->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::MinimumExpanding);
    errorLabel->setFixedWidth(390);
    errorLabel->setFixedHeight(500);

    errorLayout->addWidget(errorLabel);
    frameErrorLabel->setLayout(errorLayout);
    infoFormErrorLayout->addWidget(frameErrorLabel);

    interactiveLayout->addLayout(infoFormErrorLayout);

    frameInteractiveShiftEnd->setLayout(interactiveLayout);
    shiftEndLayout->addWidget(frameInteractiveShiftEnd);

    frameShiftEnd->setLayout(shiftEndLayout);

    createShiftEndInfo();
    CreateForm();
}


void MainWindow::printEndShift()
{
    QMessageBox::information(this, "Tisk Denní Uzávěrky", "Tisk probíhá, odsouhlaste tlačítkem.");
}


void MainWindow::createHistoryOrdersPage()
{
    if (!historyOrdersLayout) {
        historyOrdersLayout = new QVBoxLayout(frameHistoryOrders);
        frameHistoryOrders->setLayout(historyOrdersLayout);
    }

    scrollArea = new QScrollArea(frameHistoryOrders);
    scrollArea->setWidgetResizable(true);

    scrollableWidget = new QWidget(scrollArea);
    scrollableLayout = new QVBoxLayout(scrollableWidget);

    scrollArea->setWidget(scrollableWidget);
    historyOrdersLayout->addWidget(scrollArea);

    createHeaderRow();

    QVector<QVariantMap> orders = loadOrders();
    for (int i = 0; i < orders.size(); ++i) {
        createOrderRow(orders[i], i);
    }

    scrollableWidget->setLayout(scrollableLayout);
}


void MainWindow::createHeaderRow()
{
    QStringList headers = {"Přijato", "Stav objednávky", "Objednávka", "Zákazník"};

    QHBoxLayout *headerLayout = new QHBoxLayout;

    int headerHeight = 40;

    for (const QString &text : headers) {
        QLabel *label = new QLabel(text);
        label->setStyleSheet("font: bold 19px Helvetica; color: white; padding: 5px;");
        label->setAlignment(Qt::AlignLeft | Qt::AlignVCenter);
        label->setFixedHeight(headerHeight);
        headerLayout->addWidget(label);
    }

    QWidget *headerFrame = new QWidget(scrollableWidget);
    headerFrame->setFixedHeight(headerHeight);
    headerFrame->setLayout(headerLayout);

    if (QVBoxLayout *scrollableVBoxLayout = qobject_cast<QVBoxLayout*>(scrollableLayout)) {
        scrollableVBoxLayout->setAlignment(Qt::AlignTop);
    }

    scrollableLayout->addWidget(headerFrame);
}


void MainWindow::createOrderRow(QVariantMap order, int index)
{
    QString bgColor = (index % 2 == 0) ? "#F0F0F0" : "#D0D0D0";

    QWidget *rowFrame = new QWidget(scrollableWidget);
    rowFrame->setStyleSheet("background-color: " + bgColor + "; padding: 5px;");
    QHBoxLayout *rowLayout = new QHBoxLayout(rowFrame);

    QString dateTimeOrder = order["datetime"].toString();
    QLabel *datetimeLabel = new QLabel(dateTimeOrder, rowFrame);
    datetimeLabel->setStyleSheet("color: black; font: 18px; Helvetica;");
    rowLayout->addWidget(datetimeLabel);

    QString statusPriceText = QString("Stav: %1\nCena: %2\nDoprava: %3")
                                  .arg(order["status"].toString())
                                  .arg(order["total_price"].toString())
                                  .arg(order["delivery"].toString());
    QLabel *statusLabel = new QLabel(statusPriceText, rowFrame);
    statusLabel->setStyleSheet("color: black; font: 18px; Helvetica;");
    rowLayout->addWidget(statusLabel);

    QStringList items;
    for (const QVariant &product : order["products"].toList()) {
        QVariantMap item = product.toMap();
        items.append(QString(" • %1 (%2)").arg(item["name"].toString()).arg(item["price"].toString()));
    }
    QLabel *itemsLabel = new QLabel(items.join("\n"), rowFrame);
    itemsLabel->setStyleSheet("color: black; font: 18px; Helvetica;");
    rowLayout->addWidget(itemsLabel);

    QString customerInfo = QString("%1\n%2\nTel.: %3\nCena: %4")
                               .arg(order["customer"].toMap()["name"].toString())
                               .arg(order["customer"].toMap()["address"].toString())
                               .arg(order["customer"].toMap()["phone"].toString())
                               .arg(order["total_price"].toString());
    QLabel *customerLabel = new QLabel(customerInfo, rowFrame);
    customerLabel->setStyleSheet("color: black; font: 18px; Helvetica;");
    rowLayout->addWidget(customerLabel);

    rowFrame->setLayout(rowLayout);

    scrollableLayout->addWidget(rowFrame);

    createContextMenu(rowFrame, order);
}

void MainWindow::createContextMenu(QWidget *rowFrame, const QVariantMap &order)
{
    auto showContextMenu = [=](const QPoint &pos) {
        QMenu *contextMenu = new QMenu(this);
        contextMenu->setStyleSheet("font: 18pt 'Helvetica'; background-color: #707070; color: white;");

        QAction *printAction = new QAction("Tisk objednávky", contextMenu);
        connect(printAction, &QAction::triggered, this, [=]() {
            printOrder();
        });
        contextMenu->addAction(printAction);

        QMenu *deliveryMenu = contextMenu->addMenu("Změnit rozvoz");
        deliveryMenu->setStyleSheet("font: 18pt 'Helvetica';");

        QStringList deliveryOptions = {"R1", "R2", "R3", "R4", "R5", "R6", "Bistro"};
        for (const QString &delivery : deliveryOptions) {
            QAction *deliveryAction = new QAction(delivery, deliveryMenu);
            connect(deliveryAction, &QAction::triggered, this, [=]() {
                changeDelivery(delivery, order["id"].toInt());
            });
            deliveryMenu->addAction(deliveryAction);
        }

        contextMenu->exec(rowFrame->mapToGlobal(pos));
    };

    rowFrame->setContextMenuPolicy(Qt::CustomContextMenu);
    connect(rowFrame, &QWidget::customContextMenuRequested, this, showContextMenu);
}

void MainWindow::changeDelivery(const QString &deliveryName, int orderId)
{
    QVector<QVariantMap> orders = loadOrders();
    QVariantMap changedOrder;
    QString originDelivery;

    for (QVariantMap &order : orders) {
        if (order["id"].toInt() == orderId) {
            originDelivery = order["delivery"].toString();
            changedOrder = order;
            break;
        }
    }

    if (originDelivery.isEmpty() || originDelivery == "Neznámý" || changedOrder.isEmpty()) {
        return;
    }

    setDelivery(deliveryName, orderId);

    int totalPrice = changedOrder["total_price"].toString().replace("Kč", "").trimmed().toInt();

    if (originDelivery == "Bistro") {
        varTakeAwaySum -= totalPrice;
    } else {
        int originIndex = originDelivery.mid(1).toInt();
        varDictDeliveries[originIndex] -= totalPrice;
    }

    varFinalSum -= totalPrice;
    UpdateFramesList();
}


void MainWindow::createActiveOrdersPage()
{
    if (!activeOrdersLayout) {
        activeOrdersLayout = new QVBoxLayout(frameActiveOrders);
        frameActiveOrders->setLayout(activeOrdersLayout);
    }

    activeScrollArea = new QScrollArea(frameActiveOrders);
    activeScrollArea->setWidgetResizable(true);

    activeScrollableWidget = new QWidget(activeScrollArea);
    activeScrollableLayout = new QVBoxLayout(activeScrollableWidget);

    activeScrollArea->setWidget(activeScrollableWidget);
    activeOrdersLayout->addWidget(activeScrollArea);

    createActiveHeaderRow();

    QVector<QVariantMap> orders = loadOrders();
    std::sort(orders.begin(), orders.end(), [](const QVariantMap &a, const QVariantMap &b) {
        bool isANeovereno = (a["status"].toString() == "Neověřeno");
        bool isBNeovereno = (b["status"].toString() == "Neověřeno");

        if (isANeovereno != isBNeovereno) {
            return isANeovereno;
        }

        QDateTime dateTimeA = QDateTime::fromString(a["datetime"].toString(), "dd.MM.yyyy HH:mm:ss");
        QDateTime dateTimeB = QDateTime::fromString(b["datetime"].toString(), "dd.MM.yyyy HH:mm:ss");
        return dateTimeA < dateTimeB;
    });

    for (int i = 0; i < orders.size(); ++i) {
        if (orders[i]["status"] == "Neověřeno") {
            createActiveOrderRow(orders[i], i);
        }
    }

    for (int i = orders.size(); i < (orders.size()*2); ++i) {
        if (orders[i-orders.size()]["status"] == "Ověřeno" && orders[i-orders.size()]["delivery"] == "Neznámý") {
            createActiveOrderRow(orders[i-orders.size()], i);
        }
    }

    activeScrollableWidget->setLayout(activeScrollableLayout);
}


void MainWindow::createActiveHeaderRow()
{
    QStringList headers = {"Přijato", "Objednávka", "Stav doručení", "Zákazník", "Volby"};

    QHBoxLayout *headerLayout = new QHBoxLayout;

    int headerHeight = 40;

    for (const QString &text : headers) {
        QLabel *label = new QLabel(text);
        label->setStyleSheet("font: bold 19px Helvetica; color: white; padding: 5px;");
        label->setAlignment(Qt::AlignLeft | Qt::AlignVCenter);
        label->setFixedHeight(headerHeight);
        headerLayout->addWidget(label);
    }

    QWidget *headerFrame = new QWidget(activeScrollableWidget);
    headerFrame->setFixedHeight(headerHeight);
    headerFrame->setLayout(headerLayout);

    if (QVBoxLayout *activeVBoxLayout = qobject_cast<QVBoxLayout*>(activeScrollableLayout)) {
        activeVBoxLayout->setAlignment(Qt::AlignTop);
    }

    activeScrollableLayout->addWidget(headerFrame);
}



void MainWindow::createActiveOrderRow(QVariantMap order, int index)
{
    QString bgColor = (order["status"].toString() == "Neověřeno") ? "#FFAAAA" : "#AAFFAA";

    QWidget *rowFrame = new QWidget(activeScrollableWidget);
    rowFrame->setStyleSheet("background-color: " + bgColor + "; padding: 5px;");
    QHBoxLayout *rowLayout = new QHBoxLayout(rowFrame);

    QString dateTimeOrder = order["datetime"].toString().replace(" ", "\n\n   ");
    QLabel *datetimeLabel = new QLabel(dateTimeOrder, rowFrame);
    datetimeLabel->setStyleSheet("color: black; font: 18px; Helvetica;");
    rowLayout->addWidget(datetimeLabel);

    QStringList items;
    for (const QVariant &product : order["products"].toList()) {
        QVariantMap item = product.toMap();
        items.append(QString(" • %1 (%2)").arg(item["name"].toString()).arg(item["price"].toString()));
    }
    QLabel *itemsLabel = new QLabel(items.join("\n"), rowFrame);
    itemsLabel->setStyleSheet("color: black; font: 18px; Helvetica;");
    rowLayout->addWidget(itemsLabel);

    QString statusText = QString("Stav: %1\nCena: %2\nDoprava: %3")
                             .arg(order["status"].toString())
                             .arg(order["total_price"].toString())
                             .arg(order["delivery"].toString());
    QLabel *statusLabel = new QLabel(statusText, rowFrame);
    statusLabel->setStyleSheet("color: black; font: 18px; Helvetica;");
    rowLayout->addWidget(statusLabel);

    QString customerInfo = QString("%1\n%2\nTel.: %3")
                               .arg(order["customer"].toMap()["name"].toString())
                               .arg(order["customer"].toMap()["address"].toString())
                               .arg(order["customer"].toMap()["phone"].toString());
    QLabel *customerLabel = new QLabel(customerInfo, rowFrame);
    customerLabel->setStyleSheet("color: black; font: 18px; Helvetica;");
    rowLayout->addWidget(customerLabel);

    QWidget *buttonFrame = new QWidget(rowFrame);
    QVBoxLayout *buttonLayout = new QVBoxLayout(buttonFrame);

    QString buttonText = (order["status"] == "Ověřeno") ? "HOTOVO" : "OVĚŘIT";
    QPushButton *btnVerify = new QPushButton(buttonText, buttonFrame);
    btnVerify->setStyleSheet(btnChoice);

    if (order["status"] == "Ověřeno") {
        connect(btnVerify, &QPushButton::clicked, this, [=]() { finishOrder(order["id"].toInt()); });
    } else {
        connect(btnVerify, &QPushButton::clicked, this, [=]() { verifyOrder(btnVerify, order["id"].toInt()); });
    }

    buttonLayout->addWidget(btnVerify);

    QPushButton *btnCancel = new QPushButton("STORNO", buttonFrame);
    btnCancel->setStyleSheet(btnChoice);
    connect(btnCancel, &QPushButton::clicked, this, [=]() { cancelOrder(order["id"].toInt()); });
    buttonLayout->addWidget(btnCancel);

    QPushButton *btnPrint = new QPushButton("TISK", buttonFrame);
    btnPrint->setStyleSheet(btnChoice);
    connect(btnPrint, &QPushButton::clicked, this, &MainWindow::printOrder);
    buttonLayout->addWidget(btnPrint);

    rowLayout->addWidget(buttonFrame);
    activeScrollableLayout->addWidget(rowFrame);
}


void MainWindow::UpdateFramesList()
{
    if (activeScrollableLayout) {
        QLayoutItem *item;
        while ((item = activeScrollableLayout->takeAt(0)) != nullptr) {
            if (item->widget()) {
                item->widget()->setParent(nullptr);
                item->widget()->deleteLater();
            }
            delete item;
        }
    }

    createActiveHeaderRow();

    QVector<QVariantMap> orders = loadOrders();
    std::sort(orders.begin(), orders.end(), [](const QVariantMap &a, const QVariantMap &b) {
        bool isANeovereno = (a["status"].toString() == "Neověřeno");
        bool isBNeovereno = (b["status"].toString() == "Neověřeno");

        if (isANeovereno != isBNeovereno) {
            return isANeovereno;
        }

        QDateTime dateTimeA = QDateTime::fromString(a["datetime"].toString(), "dd.MM.yyyy HH:mm:ss");
        QDateTime dateTimeB = QDateTime::fromString(b["datetime"].toString(), "dd.MM.yyyy HH:mm:ss");
        return dateTimeA < dateTimeB;
    });

    for (int i = 0; i < orders.size(); ++i) {
        if (orders[i]["status"] == "Neověřeno") {
            createActiveOrderRow(orders[i], i);
        }
    }

    for (int i = orders.size(); i < (orders.size()*2); ++i) {
        if (orders[i-orders.size()]["status"] == "Ověřeno" && orders[i-orders.size()]["delivery"] == "Neznámý") {
            createActiveOrderRow(orders[i-orders.size()], i);
        }
    }

    if (historyOrdersLayout) {
        QLayoutItem *item;
        while ((item = historyOrdersLayout->takeAt(0)) != nullptr) {
            if (item->widget()) {
                item->widget()->setParent(nullptr);
                item->widget()->deleteLater();
            }
            delete item;
        }
    }

    if (!historyOrdersLayout) {
        historyOrdersLayout = new QVBoxLayout(frameHistoryOrders);
        frameHistoryOrders->setLayout(historyOrdersLayout);
    }

    createHistoryOrdersPage();

    if (activeScrollableWidget) {
        activeScrollableWidget->adjustSize();
    }

    if (frameDeliveries && frameDeliveries->layout()) {
        QLayoutItem *item;
        while ((item = frameDeliveries->layout()->takeAt(0)) != nullptr) {
            if (item->widget()) {
                item->widget()->setParent(nullptr);
                item->widget()->deleteLater();
            }
            delete item;
        }
    }

    lblAllDeliveriesInfo = new QLabel("Rozdělení podle rozvozců:", frameDeliveries);
    lblAllDeliveriesInfo->setStyleSheet("font: bold 16px Helvetica;");
    frameDeliveries->layout()->addWidget(lblAllDeliveriesInfo);

    for (auto it = varDictDeliveries.begin(); it != varDictDeliveries.end(); ++it) {
        if (it.value() > 0) {
            QLabel *deliveryLabel = new QLabel(QString("R%1 - %2 Kč").arg(it.key()).arg(it.value()), frameDeliveries);
            frameDeliveries->layout()->addWidget(deliveryLabel);
        }
    }

    if (varTakeAwaySum > 0) {
        QLabel *takeAwayLabel = new QLabel(QString("Bistro - %1 Kč").arg(varTakeAwaySum), frameDeliveries);
        frameDeliveries->layout()->addWidget(takeAwayLabel);
    }

    if (entryFields.contains("oSum")) {
        entryFields["oSum"]->setText(QString::number(varTakeAwaySum));
    }

    valueSumAll->setText(QString::number(varDailyPrice) + " Kč");
    valueSumDone->setText(QString::number(varFinalSum) + " Kč");

    valueDateTo->setText(varDateLastOrder);
    valueNumOfOrders->setText(QString::number(varOrderNum));
}



void MainWindow::setDelivery(const QString &deliveryName, int orderId)
{
    QVector<QVariantMap> orders = loadOrders();
    QVariantMap order;

    for (QVariantMap &o : orders) {
        if (o["id"].toInt() == orderId) {
            o["status"] = "Hotovo";
            o["delivery"] = deliveryName;
            order = o;
            break;
        }
    }

    int totalPrice = order["total_price"].toString().replace("Kč", "").trimmed().toInt();

    if (deliveryName == "Bistro") {
        varTakeAwaySum += totalPrice;
    } else {
        int deliveryIndex = deliveryName.mid(1).toInt();
        varDictDeliveries[deliveryIndex] += totalPrice;
    }

    varFinalSum += totalPrice;

    QVariantList orderList;
    for (const QVariantMap &o : orders) {
        orderList.append(o);
    }

    QFile file("orders.json");
    if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        QJsonDocument doc = QJsonDocument::fromVariant(orderList);
        file.write(doc.toJson(QJsonDocument::Indented));
        file.close();
    }

    if (activeScrollableWidget) {
        activeScrollableWidget->update();
    }
    UpdateFramesList();
}


void MainWindow::finishOrder(int orderId)
{
    QWidget *finishWindow = new QWidget(this, Qt::Dialog);
    finishWindow->setWindowTitle("Vyberte druh rozvozu");
    finishWindow->setStyleSheet("background-color: #505050;");
    finishWindow->resize(800, 400);
    finishWindow->setWindowModality(Qt::ApplicationModal);

    QVBoxLayout *mainLayout = new QVBoxLayout(finishWindow);

    QLabel *titleLabel = new QLabel("Vyberte druh rozvozu:");
    titleLabel->setStyleSheet("font: bold 20px Helvetica;");
    titleLabel->setMaximumHeight(40);
    titleLabel->setAlignment(Qt::AlignCenter);
    mainLayout->addWidget(titleLabel);

    QHBoxLayout *splitLayout = new QHBoxLayout();

    QWidget *leftFrame = new QWidget(finishWindow);
    QVBoxLayout *leftLayout = new QVBoxLayout(leftFrame);
    leftLayout->setAlignment(Qt::AlignCenter);

    QPushButton *btnTakeAway = new QPushButton("Odběr na\nbistru");
    btnTakeAway->setFixedSize(250, 150);
    btnTakeAway->setStyleSheet("font: bold 18px Helvetica; background-color: #97c2f7; color: black;");
    connect(btnTakeAway, &QPushButton::clicked, [=]() {
        setDelivery("Bistro", orderId);
        finishWindow->close();
    });
    leftLayout->addWidget(btnTakeAway);
    splitLayout->addWidget(leftFrame);

    QWidget *rightFrame = new QWidget(finishWindow);
    QVBoxLayout *rightMainLayout = new QVBoxLayout(rightFrame);
    rightMainLayout->setAlignment(Qt::AlignCenter);

    QGridLayout *gridLayout = new QGridLayout();

    QStringList deliveryNames = {"R1", "R2", "R3", "R4", "R5", "R6"};
    int row = 0;
    for (int i = 0; i < deliveryNames.size(); ++i) {
        QPushButton *btn = new QPushButton(deliveryNames[i]);
        btn->setFixedSize(180, 60);
        btn->setStyleSheet("font: bold 18px Helvetica; background-color: #97c2f7; color: black;");
        connect(btn, &QPushButton::clicked, [=]() {
            setDelivery(deliveryNames[i], orderId);
            finishWindow->close();
        });

        int column = (i < 3) ? 0 : 1;
        int rowIndex = (i % 3);
        gridLayout->addWidget(btn, rowIndex, column, Qt::AlignCenter);
    }

    rightMainLayout->addLayout(gridLayout);
    splitLayout->addWidget(rightFrame);

    mainLayout->addLayout(splitLayout);

    finishWindow->setLayout(mainLayout);
    finishWindow->show();
}



void MainWindow::verifyOrder(QPushButton *btn, int orderId)
{
    btn->setText("HOTOVO");
    connect(btn, &QPushButton::clicked, this, [=]() { finishOrder(orderId); });

    QVector<QVariantMap> orders = loadOrders();
    bool orderFound = false;

    for (QVariantMap &order : orders) {
        if (order["id"].toInt() == orderId) {
            order["status"] = "Ověřeno";
            orderFound = true;
            break;
        }
    }

    if (!orderFound) return;

    QVariantList orderList;
    for (const QVariantMap &order : orders) {
        orderList.append(order);
    }

    QFile file("orders.json");
    if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        QJsonDocument doc = QJsonDocument::fromVariant(orderList);
        file.write(doc.toJson(QJsonDocument::Indented));
        file.close();
    }

    UpdateFramesList();
}


void MainWindow::cancelOrder(int orderId)
{
    QMessageBox::StandardButton reply;
    reply = QMessageBox::question(this, "Zrušit objednávku", "Opravdu chcete objednávku stornovat?",
                                  QMessageBox::Yes | QMessageBox::No);

    if (reply == QMessageBox::No)
        return;

    QVector<QVariantMap> orders = loadOrders();
    bool orderFound = false;

    for (QVariantMap &order : orders) {
        if (order["id"].toInt() == orderId) {
            order["status"] = "Zrušeno";
            order["delivery"] = "Nedoručeno";
            orderFound = true;
            break;
        }
    }

    if (!orderFound) return;

    QVariantList orderList;
    for (const QVariantMap &order : orders) {
        orderList.append(order);
    }

    QFile file("orders.json");
    if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        QJsonDocument doc = QJsonDocument::fromVariant(orderList);
        file.write(doc.toJson(QJsonDocument::Indented));
        file.close();
    }

    UpdateFramesList();
}




void MainWindow::generateRandomOrder()
{
    QVector<QVariantMap> orders = loadOrders();

    static int order_id_unique = 0;
    for (const QVariantMap &order : orders) {
        int existingId = order["id"].toInt();
        if (existingId > order_id_unique) {
            order_id_unique = existingId;
        }
    }

    order_id_unique++;

    QString name = names.at(QRandomGenerator::global()->bounded(names.size())) + " " +
                   surnames.at(QRandomGenerator::global()->bounded(surnames.size()));
    QString village = villages.at(QRandomGenerator::global()->bounded(villages.size()));
    QString address = QString("%1 %2, %3")
                          .arg(village)
                          .arg(QRandomGenerator::global()->bounded(1, 501))
                          .arg(village);
    QString phone = QString("%1 %2 %3")
                        .arg(QRandomGenerator::global()->bounded(700, 800))
                        .arg(QRandomGenerator::global()->bounded(0, 1000), 3, 10, QChar('0'))
                        .arg(QRandomGenerator::global()->bounded(0, 1000), 3, 10, QChar('0'));

    int numProducts = QRandomGenerator::global()->bounded(1, 9);
    QJsonArray productsArray;
    int totalPrice = 0;

    QVector<QPair<QString, QString>> selectedProducts;
    while (selectedProducts.size() < numProducts) {
        int productIndex = QRandomGenerator::global()->bounded(product_list.size());
        selectedProducts.push_back(product_list[productIndex]);
    }

    for (const auto &p : selectedProducts) {
        QString productName = p.first;
        QString productPriceStr = p.second;

        bool ok;
        int priceValue = productPriceStr.split(" ").first().toInt(&ok);
        if (!ok) {
            qWarning() << "Error: Could not parse price from" << productPriceStr;
            continue;
        }
        totalPrice += priceValue;

        QJsonObject product;
        product["name"] = productName;
        product["price"] = productPriceStr;

        productsArray.append(product);
    }

    QString totalPriceStr = QString::number(totalPrice) + " Kč";
    QString status = (QRandomGenerator::global()->bounded(2) == 0) ? "Neověřeno" : "Ověřeno";
    QString delivery = "Neznámý";

    QVariantMap newOrder;
    newOrder["id"] = order_id_unique;
    newOrder["datetime"] = QDateTime::currentDateTime().toString("dd.MM.yyyy HH:mm:ss");
    newOrder["status"] = status;
    newOrder["total_price"] = totalPriceStr;
    newOrder["delivery"] = delivery;

    QVariantMap customer;
    customer["name"] = name;
    customer["address"] = address;
    customer["phone"] = phone;
    newOrder["customer"] = customer;

    QVariantList productsList;
    for (const auto &p : selectedProducts) {
        QVariantMap product;
        product["name"] = p.first;
        product["price"] = p.second;
        productsList.append(product);
    }
    newOrder["products"] = productsList;

    orders.append(newOrder);

    QFile file("orders.json");
    if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        QJsonArray jsonArray;
        for (const QVariantMap &order : orders) {
            jsonArray.append(QJsonObject::fromVariantMap(order));
        }
        QJsonDocument doc(jsonArray);
        file.write(doc.toJson(QJsonDocument::Indented));
        file.close();
    } else {
        qWarning() << "Failed to open file for writing.";
    }

    varDailyPrice += totalPrice;
    if (varOrderNum < 1) {
        varDateFirstOrder = newOrder["datetime"].toString();
        valueDateFrom->setText(varDateFirstOrder);
    }
    varDateLastOrder = newOrder["datetime"].toString();
    varOrderNum++;

    UpdateFramesList();
}
