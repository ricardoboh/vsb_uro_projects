#ifndef ORDERS_H
#define ORDERS_H

#include <QVector>
#include <QVariantMap>
#include <QString>

QVector<QVariantMap> loadOrders();

extern const QStringList names;
extern const QStringList surnames;
extern const QVector<QPair<QString, QString>> product_list;
extern const QStringList villages;

#endif // ORDERS_H
