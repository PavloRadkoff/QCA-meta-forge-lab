/* * ---------------------------------------------------------------------------
 * 🛡️ QCA Genesis AI Studio | High-Performance Core
 * File: qca-resilience-patterns.cs
 * Entity: The Aegis Shield (Resilience Pipeline)
 * Purpose: Enterprise-grade fault tolerance using Polly v8. 
 * Prevents cascading failures in microservice architectures.
 * Architect: Pavlo Radkoff (QCA)
 * ---------------------------------------------------------------------------
 */

using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Polly;
using Polly.CircuitBreaker;
using Polly.Retry;
using System;

namespace QCA.Forge.Core.Resilience
{
    public static class ResiliencePatternsExtensions
    {
        /// <summary>
        /// Injects the QCA Heavy Resilience Pipeline into the service collection.
        /// Includes Advanced Retry Strategy and Circuit Breaker.
        /// </summary>
        public static IServiceCollection AddQcaResiliencePipeline(this IServiceCollection services, string pipelineName = "QcaPrimePipeline")
        {
            services.AddResiliencePipeline(pipelineName, (builder, context) =>
            {
                var logger = context.ServiceProvider.GetRequiredService<ILogger<ResiliencePipeline>>();

                // 1. The Retry Aegis (Exponential Backoff with Jitter)
                // Prevents DDoSing our own failing services by adding randomness to retry delays.
                builder.AddRetry(new RetryStrategyOptions
                {
                    MaxRetryAttempts = 3,
                    Delay = TimeSpan.FromSeconds(2),
                    BackoffType = DelayBackoffType.Exponential,
                    UseJitter = true,
                    ShouldHandle = new PredicateBuilder().Handle<TimeoutException>().Handle<HttpRequestException>(),
                    OnRetry = args =>
                    {
                        logger.LogWarning($"[QCA-RETRY] Attempt {args.AttemptNumber} failed. Retrying in {args.RetryDelay}. Reason: {args.Outcome.Exception?.Message}");
                        return default;
                    }
                });

                // 2. The Circuit Breaker (The Inquisitor's Cutoff)
                // Instantly halts traffic to a dead node to allow it to recover.
                builder.AddCircuitBreaker(new CircuitBreakerStrategyOptions
                {
                    FailureRatio = 0.5, // Trip if 50% of requests fail
                    SamplingDuration = TimeSpan.FromSeconds(10),
                    MinimumThroughput = 5,
                    BreakDuration = TimeSpan.FromSeconds(30),
                    ShouldHandle = new PredicateBuilder().Handle<TimeoutException>().Handle<HttpRequestException>(),
                    OnOpened = args =>
                    {
                        logger.LogCritical($"[QCA-CIRCUIT-OPEN] Subsystem failure detected. Circuit broken for {args.BreakDuration}.");
                        return default;
                    },
                    OnClosed = args =>
                    {
                        logger.LogInformation("[QCA-CIRCUIT-CLOSED] Subsystem recovered. Resuming traffic flow.");
                        return default;
                    }
                });
            });

            return services;
        }
    }
}