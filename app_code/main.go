package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"

	"go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc"
	"go.opentelemetry.io/otel/metric"
	sdkmetric "go.opentelemetry.io/otel/sdk/metric"
	"go.opentelemetry.io/otel/sdk/resource"
	semconv "go.opentelemetry.io/otel/semconv/v1.24.0"
)

var counter metric.Int64Counter

func main() {
	ctx := context.Background()
	shutdown := setupCounter(ctx)
	defer shutdown(ctx)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
		log.Printf("defaulting to port %s", port)
	}

	http.HandleFunc("/", handler)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}

func handler(w http.ResponseWriter, r *http.Request) {
	counter.Add(context.Background(), 100)
	fmt.Fprintln(w, "Incremented santash_run_counter_total metric!")
}

func setupCounter(ctx context.Context) func(context.Context) error {
	serviceName := os.Getenv("K_SERVICE")
	if serviceName == "" {
		serviceName = "cloud-run-app"
	}
	r, err := resource.Merge(
		resource.Default(),
		resource.NewWithAttributes(
			semconv.SchemaURL,
			semconv.ServiceName(serviceName),
		),
	)
	if err != nil {
		log.Fatalf("Error creating resource: %v", err)
	}

	exporter, err := otlpmetricgrpc.New(ctx,
		otlpmetricgrpc.WithInsecure(),
	)
	if err != nil {
		log.Fatalf("Error creating exporter: %s", err)
	}
	provider := sdkmetric.NewMeterProvider(
		sdkmetric.WithReader(sdkmetric.NewPeriodicReader(exporter)),
		sdkmetric.WithResource(r),
	)

	meter := provider.Meter("example.com/metrics")
	counter, err = meter.Int64Counter("santash-run-counter")
	if err != nil {
		log.Fatalf("Error creating counter: %s", err)
	}
	return provider.Shutdown
}