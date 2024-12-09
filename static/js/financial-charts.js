document.addEventListener('DOMContentLoaded', function () {
    // Daily Chart
    function processDailyData() {
        const labels = [];
        const revenues = [];
        const expenses = [];
        const tooltipData = [];

        for (let i = 0; i < window.transactions.length; i++) {
            const transaction = window.transactions[i];
            const date = new Date(transaction.booking_date_time);
            const dateStr = date.toLocaleDateString();

            // Find index of the current date in labels
            let dateIndex = labels.indexOf(dateStr);
            if (dateIndex === -1) {
                labels.push(dateStr);
                dateIndex = labels.length - 1;
                revenues[dateIndex] = 0; // Initialize revenues
                expenses[dateIndex] = 0; // Initialize expenses
            }

            // Update revenues or expenses
            if (transaction.amount > 0) {
                revenues[dateIndex] += transaction.amount;
            } else {
                expenses[dateIndex] += Math.abs(transaction.amount);
            }

            // Tooltip data for the day
            if (!tooltipData[dateIndex]) tooltipData[dateIndex] = [];
            tooltipData[dateIndex].push({
                label: transaction.label,
                amount: transaction.amount
            });
        }

        return { labels, revenues, expenses, tooltipData };
    }

    const balanceCtx = document.getElementById('daily-chart').getContext('2d');
    const { labels, revenues, expenses, tooltipData } = processDailyData();

    new Chart(balanceCtx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: '💰',
                    data: revenues,
                    backgroundColor: 'rgba(75, 192, 75, 0.7)',
                    borderColor: 'rgb(75, 192, 75)',
                    borderWidth: 1
                },
                {
                    label: '💸',
                    data: expenses,
                    backgroundColor: 'rgba(255, 99, 132, 0.7)',
                    borderColor: 'rgb(255, 99, 132)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: false,
                    text: 'Daily Revenues and Expenses'
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const index = context.dataIndex;
                            const datasetIndex = context.datasetIndex;
                            const isRevenue = datasetIndex === 0;
                            const transactionList = tooltipData[index] || [];
                            const filtered = transactionList.filter(t =>
                                isRevenue ? t.amount > 0 : t.amount < 0
                            );
                            const total = filtered.reduce((acc, t) => acc + t.amount, 0);
                            return `${total.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')} € `;
                        }
                    }
                },
                legend: {
                    display: true,
                    position: "top",
                    align: "middle"
                }
            },
            scales: {
                x: {
                    stacked: true // Optional: Stacked bars for easier comparison
                },
                y: {
                    title: {
                        display: false,
                        text: 'Amount (€)'
                    }
                }
            }
        }
    });


    // Monthly Chart
    function processMonthlyData() {
        const labels = [];
        const revenues = [];
        const expenses = [];
        const tooltipData = [];

        for (let i = 0; i < window.transactions.length; i++) {
            const transaction = window.transactions[i];
            const date = new Date(transaction.booking_date_time);
            const monthStr = date.toLocaleDateString('default', { month: 'long', year: 'numeric' });

            // Find index of the current month in labels
            let monthIndex = labels.indexOf(monthStr);
            if (monthIndex === -1) {
                labels.push(monthStr);
                monthIndex = labels.length - 1;
                revenues[monthIndex] = 0; // Initialize revenues
                expenses[monthIndex] = 0; // Initialize expenses
            }

            // Update revenues or expenses
            if (transaction.amount > 0) {
                revenues[monthIndex] += transaction.amount;
            } else {
                expenses[monthIndex] += Math.abs(transaction.amount);
            }

            // Tooltip data for the month
            if (!tooltipData[monthIndex]) tooltipData[monthIndex] = [];
            tooltipData[monthIndex].push({
                label: transaction.label,
                amount: transaction.amount
            });
        }

        return { labels, revenues, expenses, tooltipData };
    }

    const monthlyCtx = document.getElementById('monthly-chart').getContext('2d');
    const { labels: monthlyLabels, revenues: monthlyRevenues, expenses: monthlyExpenses, tooltipData: monthlyTooltipData } = processMonthlyData();

    new Chart(monthlyCtx, {
        type: 'bar',
        data: {
            labels: monthlyLabels,
            datasets: [
                {
                    label: '💰',
                    data: monthlyRevenues,
                    backgroundColor: 'rgba(75, 192, 75, 0.7)',
                    borderColor: 'rgb(75, 192, 75)',
                    borderWidth: 1
                },
                {
                    label: '💸',
                    data: monthlyExpenses,
                    backgroundColor: 'rgba(255, 99, 132, 0.7)',
                    borderColor: 'rgb(255, 99, 132)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: false,
                    text: 'Monthly Revenues and Expenses'
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const index = context.dataIndex;
                            const datasetIndex = context.datasetIndex;
                            const isRevenue = datasetIndex === 0;
                            const transactionList = monthlyTooltipData[index] || [];
                            const filtered = transactionList.filter(t =>
                                isRevenue ? t.amount > 0 : t.amount < 0
                            );
                            const total = filtered.reduce((acc, t) => acc + t.amount, 0);
                            return `${total.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')} € `;
                        }
                    }
                },
                legend: {
                    display: true,
                    position: "top",
                    align: "middle"
                }
            },
            scales: {
                x: {
                    stacked: true // Optional: Stacked bars for easier comparison
                },
                y: {
                    title: {
                        display: false,
                        text: 'Amount (€)'
                    }
                }
            }
        }
    });


    // Category Chart
    function updateCategoriesList(labels, amounts) {
        element = document.getElementById("categories");

        while (element.firstChild) {
            element.removeChild(element.firstChild);
        }

        for (let i = 0; i < labels.length; i++) {
            const category = labels[i];
            const amount = amounts[i];
            const el = document.createElement("p");
            el.innerHTML = `<p>${category}</p><p class="bold">${amount.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')} €</p>`;
            element.appendChild(el);
        }
    }

    function processCategoryData(timePeriod = 'all') {
        const predefinedCategories = window.labels;

        const now = new Date();
        const labels = [];
        const amounts = [];
        const tooltipData = [];
    
        // Filter transactions based on time period
        const filteredTransactions = window.transactions.filter(transaction => {
            const transactionDate = new Date(transaction.booking_date_time);
            switch(timePeriod) {
                case '1d':
                    return (now - transactionDate) / (1000 * 60 * 60 * 24) < 1;
                case '7d':
                    return (now - transactionDate) / (1000 * 60 * 60 * 24) <= 7;
                case '30d':
                    return (now - transactionDate) / (1000 * 60 * 60 * 24) <= 30;
                default:
                    return true;
            }
        });
    
        // Track transactions that are categorized
        const categorizedTransactions = new Set();
    
        // Process predefined categories
        for (const category in predefinedCategories) {
            labels.push(category);
    
            // Filter transactions for the current category
            const categoryTransactions = filteredTransactions.filter(transaction => {
                const keywords = predefinedCategories[category];
                const isInCategory = transaction.amount < 0 && keywords.some(keyword => transaction.label.toUpperCase().includes(keyword));
                if (isInCategory) categorizedTransactions.add(transaction);
                return isInCategory;
            });
    
            // Calculate total expenses for the category
            const totalAmount = categoryTransactions.reduce((sum, transaction) => sum + Math.abs(transaction.amount), 0);
            amounts.push(totalAmount);
    
            // Collect tooltip data for the category
            tooltipData.push(categoryTransactions.map(transaction => ({
                label: transaction.label,
                amount: transaction.amount
            })));
        }
    
        // Process "Autres" (Other) category
        labels.push("📝 • Autres");
        const otherTransactions = filteredTransactions.filter(transaction => !categorizedTransactions.has(transaction) && transaction.amount < 0);
        const otherTotalAmount = otherTransactions.reduce((sum, transaction) => sum + Math.abs(transaction.amount), 0);
        amounts.push(otherTotalAmount);
        tooltipData.push(otherTransactions.map(transaction => ({
            label: transaction.label,
            amount: transaction.amount
        })));
    
        return { labels, amounts, tooltipData };
    }   
    

    const categoryCtx = document.getElementById('category-chart').getContext('2d');
    let categoryChart;

    function createCategoryChart(timePeriod = '30d') {
        const { labels: categoryLabels, amounts: categoryAmounts, tooltipData: categoryTooltipData } = processCategoryData(timePeriod);
        updateCategoriesList(categoryLabels, categoryAmounts);

        // Destroy existing chart if it exists
        if (categoryChart) {
            categoryChart.destroy();
        }

        categoryChart = new Chart(categoryCtx, {
            type: 'doughnut',
            data: {
                labels: categoryLabels,
                datasets: [
                    {
                        label: 'Category',
                        data: categoryAmounts,
                        backgroundColor: [
                            'rgba(255, 159, 64, 0.7)',
                            'rgba(201, 203, 207, 0.7)',
                            'rgba(153, 255, 51, 0.7)',
                            'rgba(255, 102, 204, 0.7)',
                            'rgba(102, 255, 178, 0.7)',
                            'rgba(204, 102, 255, 0.7)',
                            'rgba(255, 69, 0, 0.7)',
                            'rgba(0, 128, 128, 0.7)',
                            'rgba(0, 255, 255, 0.7)',
                            'rgba(255, 182, 193, 0.7)',
                            'rgba(255, 215, 0, 0.7)',
                            'rgba(34, 139, 34, 0.7)',
                            'rgba(128, 0, 128, 0.7)',
                            'rgba(70, 130, 180, 0.7)',
                            'rgba(255, 228, 181, 0.7)',
                            'rgba(0, 191, 255, 0.7)',
                            'rgba(135, 206, 235, 0.7)',
                            'rgba(221, 160, 221, 0.7)',
                            'rgba(139, 69, 19, 0.7)',
                            'rgba(255, 99, 71, 0.7)',
                        ],
                        borderColor: [
                            'rgb(255, 159, 64)',
                            'rgb(201, 203, 207)',
                            'rgb(153, 255, 51)',
                            'rgb(255, 102, 204)',
                            'rgb(102, 255, 178)',
                            'rgb(204, 102, 255)',
                            'rgb(255, 69, 0)',
                            'rgb(0, 128, 128)',
                            'rgb(0, 255, 255)',
                            'rgb(255, 182, 193)',
                            'rgb(255, 215, 0)',
                            'rgb(34, 139, 34)',
                            'rgb(128, 0, 128)',
                            'rgb(70, 130, 180)',
                            'rgb(255, 228, 181)',
                            'rgb(0, 191, 255)',
                            'rgb(135, 206, 235)',
                            'rgb(221, 160, 221)',
                            'rgb(139, 69, 19)',
                            'rgb(255, 99, 71)',
                        ],                                         
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: false,
                        text: 'Category Expenses'
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const index = context.dataIndex;
                                const transactionList = categoryTooltipData[index] || [];
                                const total = transactionList.reduce((acc, t) => acc + t.amount, 0);
                                return `${total.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')} € `;
                            }
                        }
                    },
                    legend: {
                        display: true,
                        position: "top",
                        align: "middle"
                    }
                }
            }
        });
    };

    createCategoryChart();

    document.getElementById('category-filter').addEventListener('change', function(e) {
        createCategoryChart(e.target.value);
    });


    function updateTransactionsList(timePeriod = '30d') {
        element = document.getElementById("transactions");

        while (element.firstChild) {
            element.removeChild(element.firstChild);
        }

        const transactions = window.transactions;
        transactions.reverse();

        for (let i = 0; i < transactions.length; i++) {
            const transaction = transactions[i];
            const date = new Date(transaction.booking_date_time);
            const dateStr = date.toLocaleDateString();
            const now = new Date();

            if (timePeriod === '1d' && (now - date) / (1000 * 60 * 60 * 24) >= 1) {
                continue;
            } else if (timePeriod === '7d' && (now - date) / (1000 * 60 * 60 * 24) > 7) {
                continue;
            } else if (timePeriod === '30d' && (now - date) / (1000 * 60 * 60 * 24) > 30) {
                continue;
            }

            const el = document.createElement("p");
            if (transaction.amount > 0) {
                el.innerHTML = `<p>${dateStr} • ${transaction.label}</p><p class="bold positive">+${transaction.amount.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')} €</p>`;
            } else {
                el.innerHTML = `<p>${dateStr} • ${transaction.label}</p><p class="bold negative">${transaction.amount.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')} €</p>`;
            }
            element.appendChild(el);
        }
    }

    updateTransactionsList();

    document.getElementById('transactions-filter').addEventListener('change', function(e) {
        updateTransactionsList(e.target.value);
    });
});
