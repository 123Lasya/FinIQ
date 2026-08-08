/* FinIQ - Interactive Charts & Dynamic Analytics Engine */

window.execChartInstances = {};

document.addEventListener('DOMContentLoaded', () => {
  initDashboardCharts();
  initExecutiveCharts('weekly');
});

function getThemeColors() {
  return {
    cyan: '#38BDF8',
    cyanSoft: 'rgba(56, 189, 248, 0.22)',
    teal: '#10B981',
    tealSoft: 'rgba(16, 185, 129, 0.22)',
    indigo: '#6366F1',
    indigoSoft: 'rgba(99, 102, 241, 0.22)',
    purple: '#8B5CF6',
    purpleSoft: 'rgba(139, 92, 246, 0.22)',
    amber: '#F59E0B',
    amberSoft: 'rgba(245, 158, 11, 0.22)',
    rose: '#F43F5E',
    roseSoft: 'rgba(244, 63, 94, 0.22)',
    text: '#E2E8F0',
    muted: '#94A3B8',
    grid: 'rgba(148, 163, 184, 0.16)',
    surface: '#020617'
  };
}

function createVerticalGradient(ctx, colorA, colorB) {
  const gradient = ctx.createLinearGradient(0, 0, 0, ctx.canvas.clientHeight || 280);
  gradient.addColorStop(0, colorA);
  gradient.addColorStop(1, colorB);
  return gradient;
}

function createHorizontalGradient(ctx, colorA, colorB) {
  const gradient = ctx.createLinearGradient(0, 0, ctx.canvas.clientWidth || 320, 0);
  gradient.addColorStop(0, colorA);
  gradient.addColorStop(1, colorB);
  return gradient;
}

function initDashboardCharts() {
  const colors = getThemeColors();

  // Chart 1: Daily Cases (Received vs Resolved)
  const ctxCases = document.getElementById('chart-daily-cases');
  if (ctxCases) {
    const chartCtx = ctxCases.getContext('2d');
    new Chart(ctxCases, {
      type: 'bar',
      data: {
        labels: ['02 Aug', '03 Aug', '04 Aug', '05 Aug', '06 Aug', '07 Aug', '08 Aug'],
        datasets: [
          {
            label: 'Received',
            data: [180, 195, 210, 240, 225, 250, 246],
            backgroundColor: createVerticalGradient(chartCtx, 'rgba(56, 189, 248, 0.72)', 'rgba(99, 102, 241, 0.24)'),
            borderColor: colors.cyan,
            borderWidth: 2,
            borderRadius: 10,
            borderSkipped: false,
            hoverBackgroundColor: 'rgba(56, 189, 248, 0.95)',
            hoverBorderColor: colors.cyan,
            hoverBorderWidth: 1.5,
            hoverOffset: 0,
            barPercentage: 0.8,
            categoryPercentage: 0.8,
            maxBarThickness: 34,
            shadowColor: 'rgba(56, 189, 248, 0.25)',
            shadowBlur: 10
          },
          {
            label: 'Resolved',
            data: [172, 190, 205, 235, 220, 242, 212],
            backgroundColor: createVerticalGradient(chartCtx, 'rgba(16, 185, 129, 0.68)', 'rgba(56, 189, 248, 0.2)'),
            borderColor: colors.teal,
            borderWidth: 2,
            borderRadius: 10,
            borderSkipped: false,
            hoverBackgroundColor: 'rgba(16, 185, 129, 0.95)',
            hoverBorderColor: colors.teal,
            hoverBorderWidth: 1.5,
            hoverOffset: 0,
            barPercentage: 0.8,
            categoryPercentage: 0.8,
            maxBarThickness: 34,
            shadowColor: 'rgba(16, 185, 129, 0.25)',
            shadowBlur: 10
          }
        ]
      },
      options: {
        ...getCommonChartOptions({
          scales: {
            x: {
              stacked: false,
              grid: { display: false },
              ticks: { color: '#94A3B8', font: { family: 'Plus Jakarta Sans', size: 10, weight: '600' } }
            },
            y: {
              stacked: false,
              suggestedMax: 280,
              grid: { color: 'rgba(148, 163, 184, 0.16)', drawBorder: false },
              ticks: { color: '#94A3B8', font: { family: 'Plus Jakarta Sans', size: 10, weight: '600' } }
            }
          }
        }),
        layout: { padding: { top: 6, right: 6, left: 0, bottom: 0 } },
        plugins: {
          title: {
            display: true,
            text: 'Daily case intake vs resolution',
            color: '#F8FAFC',
            font: { family: 'Plus Jakarta Sans', size: 13, weight: '700' },
            padding: { bottom: 10 }
          },
          legend: {
            position: 'top',
            align: 'start',
            labels: {
              color: '#E2E8F0',
              usePointStyle: true,
              boxWidth: 10,
              boxHeight: 10,
              padding: 12,
              font: { family: 'Plus Jakarta Sans', size: 11, weight: '600' }
            }
          },
          tooltip: {
            backgroundColor: 'rgba(2, 6, 23, 0.96)',
            titleColor: '#F8FAFC',
            bodyColor: '#E2E8F0',
            borderColor: 'rgba(56, 189, 248, 0.35)',
            borderWidth: 1,
            padding: 12,
            callbacks: {
              label: (context) => `${context.dataset.label}: ${context.formattedValue} cases`
            }
          }
        }
      }
    });
  }

  // Chart 2: Fraud Categories (Doughnut)
  const ctxFraud = document.getElementById('chart-fraud-categories');
  if (ctxFraud) {
    new Chart(ctxFraud, {
      type: 'doughnut',
      data: {
        labels: ['Card Not Present (34%)', 'Account Takeover (22%)', 'Merchant Fraud (18%)', 'Duplicate Debit (14%)', 'Social Engineering (12%)'],
        datasets: [{
          data: [34, 22, 18, 14, 12],
          backgroundColor: [
            'rgba(56, 189, 248, 0.95)',
            'rgba(99, 102, 241, 0.95)',
            'rgba(139, 92, 246, 0.95)',
            'rgba(245, 158, 11, 0.95)',
            'rgba(244, 63, 94, 0.95)'
          ],
          borderWidth: 2,
          borderColor: 'rgba(2, 6, 23, 0.95)',
          hoverOffset: 10,
          spacing: 3
        }]
      },
      options: getDoughnutChartOptions({
        cutout: '70%',
        rotation: -90 * (Math.PI / 180),
        plugins: {
          legend: {
            position: 'right',
            labels: {
              color: '#E2E8F0',
              padding: 14,
              boxWidth: 12,
              boxHeight: 12,
              usePointStyle: true,
              font: { family: 'Plus Jakarta Sans', size: 11, weight: '600' }
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => `${context.label}: ${context.raw}% of fraud volume`
            }
          }
        }
      })
    });
  }

  // Chart 3: AI vs Human Decisions (Stacked Bar)
  const ctxDecision = document.getElementById('chart-decision-ownership');
  if (ctxDecision) {
    const chartCtx = ctxDecision.getContext('2d');
    new Chart(ctxDecision, {
      type: 'bar',
      data: {
        labels: ['Week 27', 'Week 28', 'Week 29', 'Week 30', 'Week 31', 'Week 32'],
        datasets: [
          {
            label: 'Autonomous (AI)',
            data: [82, 86, 88, 91, 93, 92.4],
            backgroundColor: createVerticalGradient(chartCtx, 'rgba(99, 102, 241, 0.75)', 'rgba(139, 92, 246, 0.24)'),
            borderColor: colors.indigo,
            borderWidth: 2,
            borderRadius: 8,
            barPercentage: 0.88,
            categoryPercentage: 0.82,
            maxBarThickness: 34
          },
          {
            label: 'Human Approved',
            data: [18, 14, 12, 9, 7, 7.6],
            backgroundColor: createVerticalGradient(chartCtx, 'rgba(245, 158, 11, 0.72)', 'rgba(244, 63, 94, 0.22)'),
            borderColor: colors.amber,
            borderWidth: 2,
            borderRadius: 8,
            barPercentage: 0.88,
            categoryPercentage: 0.82,
            maxBarThickness: 34
          }
        ]
      },
      options: {
        ...getCommonChartOptions({
          scales: {
            x: {
              stacked: true,
              grid: { display: false },
              ticks: { color: '#94A3B8', font: { family: 'Plus Jakarta Sans', size: 10, weight: '600' } }
            },
            y: {
              stacked: true,
              suggestedMax: 100,
              grid: { color: 'rgba(148, 163, 184, 0.16)', drawBorder: false },
              ticks: { color: '#94A3B8', font: { family: 'Plus Jakarta Sans', size: 10, weight: '600' } }
            }
          }
        }),
        layout: { padding: { top: 6, right: 6, left: 0, bottom: 0 } },
        plugins: {
          title: {
            display: true,
            text: 'Autonomous vs human-validated decisions',
            color: '#F8FAFC',
            font: { family: 'Plus Jakarta Sans', size: 13, weight: '700' },
            padding: { bottom: 10 }
          },
          legend: {
            position: 'top',
            align: 'start',
            labels: {
              color: '#E2E8F0',
              usePointStyle: true,
              boxWidth: 10,
              boxHeight: 10,
              padding: 12,
              font: { family: 'Plus Jakarta Sans', size: 11, weight: '600' }
            }
          },
          tooltip: {
            backgroundColor: 'rgba(2, 6, 23, 0.96)',
            titleColor: '#F8FAFC',
            bodyColor: '#E2E8F0',
            borderColor: 'rgba(56, 189, 248, 0.35)',
            borderWidth: 1,
            padding: 12,
            callbacks: {
              label: (context) => `${context.dataset.label}: ${context.formattedValue}%`
            }
          }
        }
      }
    });
  }

  // Chart 4: Refund Trends (Area Chart)
  const ctxRefund = document.getElementById('chart-refund-trends');
  if (ctxRefund) {
    const chartCtx = ctxRefund.getContext('2d');
    const fillGradient = createVerticalGradient(chartCtx, 'rgba(56, 189, 248, 0.38)', 'rgba(2, 6, 23, 0.03)');
    const lineGradient = createHorizontalGradient(chartCtx, 'rgba(56, 189, 248, 1)', 'rgba(16, 185, 129, 0.95)');
    new Chart(ctxRefund, {
      type: 'line',
      data: {
        labels: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
        datasets: [{
          label: 'Reversed Value (₹ Lakhs)',
          data: [14.2, 18.5, 16.8, 22.4, 21.0, 26.5, 28.4],
          borderColor: lineGradient,
          backgroundColor: fillGradient,
          fill: true,
          tension: 0.42,
          pointRadius: 4.8,
          pointHoverRadius: 6.5,
          pointHoverBackgroundColor: colors.cyan,
          pointBackgroundColor: colors.cyan,
          pointBorderColor: '#F8FAFC',
          pointBorderWidth: 2,
          borderWidth: 3,
          cubicInterpolationMode: 'monotone'
        }]
      },
      options: getCommonChartOptions({
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: '#E2E8F0',
              boxWidth: 12,
              boxHeight: 12,
              usePointStyle: true,
              font: { family: 'Plus Jakarta Sans', size: 11, weight: '600' }
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => `₹${context.raw} Lakhs reversed`
            }
          }
        }
      })
    });
  }
}

// Executive Analytics Charts with Timeframe Switcher Support
function initExecutiveCharts(timeframe = 'weekly') {
  const colors = getThemeColors();
  const dataMap = {
    daily: {
      labels: ['02 Aug', '03 Aug', '04 Aug', '05 Aug', '06 Aug', '07 Aug', '08 Aug'],
      conf: [91.2, 92.0, 92.5, 93.1, 93.4, 93.8, 94.2],
      override: [9.1, 8.8, 8.2, 7.9, 7.6, 7.2, 6.8]
    },
    weekly: {
      labels: ['W27', 'W28', 'W29', 'W30', 'W31', 'W32'],
      conf: [88.0, 89.2, 91.5, 92.1, 93.0, 93.4],
      override: [14.2, 12.0, 10.4, 8.8, 8.1, 7.6]
    },
    monthly: {
      labels: ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
      conf: [84.5, 86.8, 89.0, 91.2, 92.8, 93.4],
      override: [18.5, 15.2, 12.8, 10.1, 8.4, 7.6]
    },
    quarterly: {
      labels: ['Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026'],
      conf: [79.2, 83.4, 88.6, 91.5, 93.4],
      override: [24.1, 19.8, 13.5, 9.2, 7.6]
    }
  };

  const selectedData = dataMap[timeframe] || dataMap['weekly'];

  // Exec Chart 1: Confidence Line
  const ctxExecConf = document.getElementById('chart-exec-confidence');
  if (ctxExecConf) {
    if (window.execChartInstances.confidence) window.execChartInstances.confidence.destroy();
    const chartCtx = ctxExecConf.getContext('2d');
    const fillGradient = createVerticalGradient(chartCtx, 'rgba(16, 185, 129, 0.32)', 'rgba(2, 6, 23, 0.02)');
    window.execChartInstances.confidence = new Chart(ctxExecConf, {
      type: 'line',
      data: {
        labels: selectedData.labels,
        datasets: [{
          label: 'Calibrated AI Confidence %',
          data: selectedData.conf,
          borderColor: colors.teal,
          backgroundColor: fillGradient,
          fill: true,
          tension: 0.35,
          pointRadius: 4.5,
          pointHoverRadius: 6.5,
          pointHoverBackgroundColor: colors.teal,
          pointBackgroundColor: colors.teal,
          pointBorderColor: '#F8FAFC',
          pointBorderWidth: 2,
          borderWidth: 3
        }]
      },
      options: getCommonChartOptions()
    });
  }

  // Exec Chart 2: Override Rate Bar
  const ctxExecOver = document.getElementById('chart-exec-override');
  if (ctxExecOver) {
    if (window.execChartInstances.override) window.execChartInstances.override.destroy();
    const chartCtx = ctxExecOver.getContext('2d');
    window.execChartInstances.override = new Chart(ctxExecOver, {
      type: 'bar',
      data: {
        labels: selectedData.labels,
        datasets: [{
          label: 'Human Override Rate %',
          data: selectedData.override,
          backgroundColor: createVerticalGradient(chartCtx, colors.amberSoft, colors.roseSoft),
          borderColor: colors.amber,
          borderWidth: 1.5,
          borderRadius: 8,
          hoverBackgroundColor: 'rgba(245, 158, 11, 0.95)',
          hoverBorderColor: colors.amber,
          hoverBorderWidth: 1.3
        }]
      },
      options: getCommonChartOptions()
    });
  }

  // Exec Chart 3: Policy Usage Bar
  const ctxExecPolicy = document.getElementById('chart-exec-policy');
  if (ctxExecPolicy) {
    if (!window.execChartInstances.policy) {
      const chartCtx = ctxExecPolicy.getContext('2d');
      window.execChartInstances.policy = new Chart(ctxExecPolicy, {
        type: 'bar',
        data: {
          labels: ['Refund §4.2', 'RBI Clause 9(c)', 'Fraud SOP St.6', 'Compliance §11.4', 'Chargeback GL 3.1'],
          datasets: [{
            label: 'Citation Frequency',
            data: [412, 366, 281, 205, 132],
            backgroundColor: createHorizontalGradient(chartCtx, 'rgba(56, 189, 248, 0.78)', 'rgba(139, 92, 246, 0.28)'),
            borderColor: colors.cyan,
            borderWidth: 2,
            borderRadius: 10,
            barPercentage: 0.84,
            categoryPercentage: 0.8,
            maxBarThickness: 40,
            hoverBackgroundColor: 'rgba(99, 102, 241, 0.95)',
            hoverBorderColor: colors.indigo,
            hoverBorderWidth: 1.4,
            shadowColor: 'rgba(56, 189, 248, 0.24)',
            shadowBlur: 10
          }]
        },
        options: {
          ...getCommonChartOptions({
            scales: {
              x: {
                grid: { display: false },
                ticks: { color: '#94A3B8', font: { family: 'Plus Jakarta Sans', size: 10, weight: '600' } }
              },
              y: {
                grid: { color: 'rgba(148, 163, 184, 0.16)', drawBorder: false },
                ticks: { color: '#94A3B8', font: { family: 'Plus Jakarta Sans', size: 10, weight: '600' } },
                beginAtZero: true
              }
            }
          }),
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: (context) => `${context.raw} citations`
              }
            }
          }
        }
      });
    }
  }

  // Exec Chart 4: Simulation Alignment Pie
  const ctxExecSim = document.getElementById('chart-exec-simulation');
  if (ctxExecSim) {
    if (!window.execChartInstances.simulation) {
      window.execChartInstances.simulation = new Chart(ctxExecSim, {
        type: 'pie',
        data: {
          labels: ['Aligned with Execution (82%)', 'Revised after Simulation (12%)', 'Blocked by Guardrail (6%)'],
          datasets: [{
            data: [82, 12, 6],
            backgroundColor: [colors.teal, colors.amber, colors.rose],
            borderWidth: 2,
            borderColor: '#020617',
            hoverBackgroundColor: [colors.teal, colors.amber, colors.rose],
            hoverOffset: 8
          }]
        },
        options: getDoughnutChartOptions({ cutout: '0%' })
      });
    }
  }

  // Exec Chart 5: Regional Desk Radar
  const ctxRadar = document.getElementById('chart-exec-radar');
  if (ctxRadar) {
    if (!window.execChartInstances.radar) {
      window.execChartInstances.radar = new Chart(ctxRadar, {
        type: 'radar',
        data: {
          labels: ['SLA Speed', 'Autonomous Acc', 'Zero Trust Pass', 'RAG Relevance', 'Volume Capacity'],
          datasets: [
            { label: 'APAC-1 (Mumbai)', data: [95, 92, 94, 96, 90], borderColor: colors.cyan, backgroundColor: colors.cyanSoft, borderWidth: 2.5 },
            { label: 'US-EAST (NY)', data: [98, 94, 96, 94, 95], borderColor: colors.teal, backgroundColor: colors.tealSoft, borderWidth: 2.5 },
            { label: 'EMEA-1 (London)', data: [88, 89, 90, 92, 85], borderColor: colors.purple, backgroundColor: colors.purpleSoft, borderWidth: 2.5 }
          ]
        },
        options: getRadarChartOptions()
      });
    }
  }

  // Exec Chart 6: Dispute Channel Distribution (Doughnut)
  const ctxChannels = document.getElementById('chart-exec-channels');
  if (ctxChannels) {
    if (!window.execChartInstances.channels) {
      window.execChartInstances.channels = new Chart(ctxChannels, {
        type: 'doughnut',
        data: {
          labels: ['Mobile App (42%)', 'Net Banking (28%)', 'Contact Centre (14%)', 'Risk Engine (10%)', 'Branch (6%)'],
          datasets: [{
            data: [42, 28, 14, 10, 6],
            backgroundColor: [colors.cyan, colors.indigo, colors.teal, colors.amber, colors.purple],
            borderWidth: 2,
            borderColor: '#020617',
            hoverBackgroundColor: [colors.cyan, colors.indigo, colors.teal, colors.amber, colors.purple],
            hoverOffset: 8
          }]
        },
        options: getDoughnutChartOptions({ cutout: '65%' })
      });
    }
  }
}

function getCommonChartOptions(extra = {}) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 1400, easing: 'easeOutQuart' },
    interaction: { mode: 'index', intersect: false },
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#E2E8F0',
          padding: 14,
          boxWidth: 12,
          boxHeight: 12,
          usePointStyle: true,
          font: { family: 'Plus Jakarta Sans', size: 11, weight: '600' }
        }
      },
      tooltip: {
        backgroundColor: 'rgba(2, 6, 23, 0.96)',
        titleColor: '#F8FAFC',
        bodyColor: '#E2E8F0',
        borderColor: 'rgba(56, 189, 248, 0.35)',
        borderWidth: 1,
        padding: 12,
        displayColors: true,
        callbacks: {
          label: (context) => `${context.dataset.label}: ${context.formattedValue}`
        }
      }
    },
    scales: {
      x: {
        grid: { color: 'rgba(148, 163, 184, 0.14)', drawBorder: false },
        border: { display: false },
        ticks: { color: '#94A3B8', font: { family: 'Plus Jakarta Sans', size: 10, weight: '600' } }
      },
      y: {
        grid: { color: 'rgba(148, 163, 184, 0.14)', drawBorder: false },
        border: { display: false },
        ticks: { color: '#94A3B8', font: { family: 'Plus Jakarta Sans', size: 10, weight: '600' } },
        beginAtZero: true
      }
    },
    ...extra
  };
}

function getDoughnutChartOptions(extra = {}) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 1400, easing: 'easeOutQuart' },
    plugins: {
      legend: {
        position: 'right',
        labels: {
          color: '#E2E8F0',
          padding: 14,
          boxWidth: 12,
          boxHeight: 12,
          usePointStyle: true,
          font: { family: 'Plus Jakarta Sans', size: 11, weight: '600' }
        }
      },
      tooltip: {
        backgroundColor: 'rgba(2, 6, 23, 0.96)',
        titleColor: '#F8FAFC',
        bodyColor: '#E2E8F0',
        borderColor: 'rgba(56, 189, 248, 0.35)',
        borderWidth: 1,
        padding: 12,
        displayColors: true
      }
    },
    ...extra
  };
}

function getRadarChartOptions() {
  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 1200, easing: 'easeOutQuart' },
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#E2E8F0',
          padding: 12,
          font: { family: 'Plus Jakarta Sans', size: 11, weight: '600' }
        }
      },
      tooltip: {
        backgroundColor: 'rgba(2, 6, 23, 0.96)',
        titleColor: '#F8FAFC',
        bodyColor: '#E2E8F0',
        borderColor: 'rgba(56, 189, 248, 0.35)',
        borderWidth: 1,
        padding: 12
      }
    },
    scales: {
      r: {
        angleLines: { color: 'rgba(148, 163, 184, 0.14)' },
        grid: { color: 'rgba(148, 163, 184, 0.14)' },
        pointLabels: { color: '#94A3B8', font: { family: 'Plus Jakarta Sans', size: 10, weight: '600' } },
        ticks: { color: '#64748B', backdropColor: 'transparent' },
        suggestedMin: 80,
        suggestedMax: 100
      }
    }
  };
}
