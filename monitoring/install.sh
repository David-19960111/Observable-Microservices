#!/bin/bash
set -e

NAMESPACE="monitoring"

kubectl create namespace $NAMESPACE || true

echo "🚀 Instalando Prometheus..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/prometheus -f monitoring/prometheus/values.yaml -n $NAMESPACE

echo "📊 Instalando Grafana..."
helm repo add grafana https://grafana.github.io/helm-charts
helm install grafana grafana/grafana -f monitoring/grafana/values.yaml -n $NAMESPACE

echo "📦 Instalando Loki y Promtail..."
helm install loki grafana/loki -f monitoring/loki/values.yaml -n $NAMESPACE
helm install promtail grafana/promtail -f monitoring/loki/promtail-values.yaml -n $NAMESPACE

echo "🧭 Instalando Jaeger..."
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm install jaeger jaegertracing/jaeger -f monitoring/jaeger/values.yaml -n $NAMESPACE

echo "✅ Stack de observabilidad desplegado correctamente."
