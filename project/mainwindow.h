#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QWidget>
#include <QPushButton>
#include <QLabel>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QTabWidget>
#include <QFileDialog>
#include <QMessageBox>
#include <QMainWindow>
#include <QMap>
#include <QLineEdit>
#include <QLabel>
#include <QPushButton>
#include <QMessageBox>
#include <QMainWindow>
#include <QLineEdit>
#include <QLabel>
#include <QPushButton>
#include <QVBoxLayout>
#include <QScrollArea>

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    QString validStyle = "font: 20px Helvetica; background-color: lightgrey; color: black;";
    QString invalidStyle = "font: 20px Helvetica; background-color: red; color: white;";
    QString enabledStyle = "font: 20px Helvetica; color: black; background-color: white;";
    QString disabledStyle = "font: 20px Helvetica; color: white; background-color: #A9A9A9;";
    QString errorLabelText = "font: 16pt 'Helvetica'; color: black; background-color: lightgrey; padding-top: 30px; padding-left: 10px;";
    QString btnBackground = "font: 16pt 'Helvetica'; color: black; background-color: #87CEFA;";
    QString btnChoice = "background-color: #919191; color: black; height: 38px; font: 23px";



    // colors
    const QString light_red = "#f79797";
    const QString light_green = "#9af797";
    const QString light_yellow = "#f4f797";
    const QString light_blue = "#97c2f7";
    const QString darker_blue = "#748CAB";
    const QString light_purple = "#c597f7";

    const QString dark_red = "#f73a34";
    const QString dark_green = "#0d8701";
    const QString dark_yellow = "#d1a711";
    const QString dark_blue = "#2958cf";
    const QString dark_purple = "#a922d6";

    const QString dark_text_color = "#000000";
    const QString light_text_color = "#eee9f2";
    const QString order_row_color = "#C9C9C9";

    const QString background_color_ternary = "#CEE5F2";
    const QString background_color_secondary = "#E3B505";
    const QString background_color_primary = "#767676";

private slots:
    void logout();
    void onTabSelected(int index);
    void uploadInvoice();
    void printEndShift();
    void printOrder();
    void countEndShift();
    void makeFinalSum();
    void showErrorMessage(const QString &message);
    void showSuccessMessage();

private:
    QWidget *centralWidget;
    QWidget *headerFrame;
    QWidget *mainFrame;

    QPushButton *btnCreateOrder;
    QLabel *lblBranchName;
    QPushButton *btnLogout;

    QVBoxLayout *mainLayout;
    QHBoxLayout *headerLayout;

    void createMainPageLayout();
    void createHeaderLayout();

    QTabWidget *notebook;
    QWidget *frameActiveOrders;
    QWidget *frameHistoryOrders;
    QWidget *frameShiftEnd;

    void createNotebook();

    int varTakeAwaySum;
    int varDeferment;
    QMap<int, int> varDictDeliveries;
    int varCash;
    int varFinalSum;
    int varDailyPrice;
    int varOrderNum;
    int varCards;
    int varShopping;
    int varFoodCarts;
    QString varDateFirstOrder;
    QString varDateLastOrder;
    QString varActualDate;

    QWidget *frameGenerated;
    QLabel *lblEnd;
    QLabel *lblGenerated;
    QLabel *lblDateFrom;
    QLabel *lblDateTo;
    QLabel *lblNumOfOrders;
    QLabel *valueGenerated;
    QLabel *valueDateFrom;
    QLabel *valueDateTo;
    QLabel *valueNumOfOrders;

    QWidget *frameDeliveries;
    QLabel *lblAllDeliveriesInfo;
    QWidget *frameSumaryOfDeliveries;
    QLabel *lblSumDone;
    QLabel *lblSumAll;
    QLabel *valueSumDone;
    QLabel *valueSumAll;

    void createShiftEndInfo();

    QMap<QString, QLineEdit*> entryFields;
    QMap<QString, int> values;

    QLabel *errorLabel;
    QPushButton *btnSaveEndShift;
    QPushButton *btnCountEndShift;
    QPushButton *floatingButton;

    void EditEndShiftForm();
    void SaveEndShift();

    QWidget *frameEndFormShiftEnd;
    QMap<QString, QLabel*> labelFields;

    void CreateForm();

    QWidget *frameInteractiveShiftEnd;
    QWidget *frameButtonsShiftEnd;
    QWidget *frameEndInfoShiftEnd;
    QWidget *frameErrorLabel;

    QPushButton *btnPrintEnd;
    QPushButton *btnSaveInvoice;

    void createShiftEndPage();

    QScrollArea *scrollArea;
    QWidget *scrollableWidget;
    QVBoxLayout *scrollableLayout;
    QVBoxLayout *historyOrdersLayout;
    QVBoxLayout *shiftEndLayout;
    QVBoxLayout *activeOrdersLayout;

    void createHistoryOrdersPage();
    void createHeaderRow();
    void createOrderRow(QVariantMap order, int index);

    QScrollArea *activeScrollArea;
    QWidget *activeScrollableWidget;
    QVBoxLayout *activeScrollableLayout;

    void createActiveOrdersPage();
    void createActiveHeaderRow();
    void createActiveOrderRow(QVariantMap order, int index);

    void finishOrder(int orderId);
    void verifyOrder(QPushButton *btn, int orderId);
    void cancelOrder(int orderId);
    void setDelivery(const QString &deliveryName, int orderId);
    void createContextMenu(QWidget *rowFrame, const QVariantMap &order);
    void changeDelivery(const QString &deliveryName, int orderId);

    void UpdateFramesList();

    void generateRandomOrder();

    void resizeEvent(QResizeEvent *event);
};

#endif // MAINWINDOW_H
