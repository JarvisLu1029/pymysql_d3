// 固定的類別配色，身分不隨篩選結果重新排列
const CATEGORY_COLORS = {
    "Furniture": "#2a78d6",
    "Office Supplies": "#1baf7a",
    "Technology": "#eb6834",
};
const CATEGORY_ORDER = Object.keys(CATEGORY_COLORS);
const FALLBACK_COLOR = "#898781";

const TABLE_PAGE_SIZE = 10;
let tableState = { data: [], page: 1 };

function drawScatterplot(data) {
    const svg = d3.select("#scatter_plot"),
        width = +svg.attr("width"),
        height = +svg.attr("height"),
        margin = { top: 20, right: 24, bottom: 40, left: 56 };

    svg.selectAll("*").remove();

    const profit = data.map(d => d.profit);
    const minProfitValue = Math.min(...profit);
    const maxProfitValue = Math.max(...profit);

    const sales = data.map(d => d.sales);
    const minSalesValue = Math.min(...sales);
    const maxSalesValue = Math.max(...sales);

    const x = d3.scaleLinear()
        .domain([minSalesValue - 1000, maxSalesValue + 1000])
        .range([margin.left, width - margin.right]);

    const y = d3.scaleLinear()
        .domain([minProfitValue - 10, maxProfitValue + 20])
        .range([height - margin.bottom, margin.top]);

    const color = d => CATEGORY_COLORS[d.category] || FALLBACK_COLOR;

    // 水平格線置於資料標記之下，作為退居視覺參照
    svg.append("g")
        .attr("class", "grid")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y)
            .tickSize(-(width - margin.left - margin.right))
            .tickFormat(""))
        .call(g => g.select(".domain").remove());

    svg.append("g")
        .attr("class", "axis")
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x).ticks(6).tickFormat(d3.format("~s")));

    svg.append("g")
        .attr("class", "axis")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y).ticks(6).tickFormat(d => `${d}%`));

    svg.append("text")
        .attr("class", "axis")
        .attr("text-anchor", "middle")
        .attr("x", (margin.left + width - margin.right) / 2)
        .attr("y", height - 4)
        .attr("fill", "#898781")
        .attr("font-size", 11)
        .text("Sales（銷售額）");

    svg.append("text")
        .attr("class", "axis")
        .attr("text-anchor", "middle")
        .attr("transform", `translate(14,${(margin.top + height - margin.bottom) / 2}) rotate(-90)`)
        .attr("fill", "#898781")
        .attr("font-size", 11)
        .text("Profit Margin（利潤率）");

    const tooltip = d3.select("#scatter_tooltip");

    const dots = svg.append("g")
        .selectAll("circle")
        .data(data)
        .join("circle")
        .attr("cx", d => x(d.sales))
        .attr("cy", d => y(d.profit))
        .attr("fill", color)
        .attr("stroke", "#fcfcfb")
        .attr("stroke-width", 1.5)
        .attr("r", 4)
        .attr("cursor", "pointer")
        .on("mouseover", function (event, d) {
            tooltip
                .style("visibility", "visible")
                .html(`<strong>${d.product_name}</strong><br>
                    Sales: $${d.sales.toLocaleString()}<br>
                    Profit: ${d.profit}%<br>
                    ${d.category} / ${d.sub_category}`);
            d3.select(this).attr("r", 6);
        })
        .on("mousemove", function (event) {
            tooltip
                .style("top", (event.pageY - 40) + "px")
                .style("left", (event.pageX + 12) + "px");
        })
        .on("mouseout", function () {
            tooltip.style("visibility", "hidden");
            d3.select(this).attr("r", 4);
        });

    renderScatterLegend(data);
    renderTable([]);

    const brush = d3.brush()
        .extent([[margin.left, margin.top], [width - margin.right, height - margin.bottom]])
        .on("brush end", brushed);

    svg.append("g")
        .attr("class", "brush")
        .call(brush);

    function brushed({ selection }) {
        if (!selection) {
            dots.classed("selected", false);
            renderTable([]);
            return;
        }

        const [[x0, y0], [x1, y1]] = selection;

        const selectedData = data.filter(d =>
            x0 <= x(d.sales) && x(d.sales) <= x1 &&
            y0 <= y(d.profit) && y(d.profit) <= y1
        );

        dots.classed("selected", d =>
            selectedData.includes(d)
        );

        renderTable(selectedData);
    }
}

// 框選出的資料筆數可能很多，改用分頁避免表格撐爆版面
function renderTable(data) {
    tableState = { data, page: 1 };
    renderTablePage();
}

function renderTablePage() {
    const { data, page } = tableState;
    const totalPages = Math.max(1, Math.ceil(data.length / TABLE_PAGE_SIZE));
    tableState.page = Math.min(Math.max(page, 1), totalPages);

    const start = (tableState.page - 1) * TABLE_PAGE_SIZE;
    const pageData = data.slice(start, start + TABLE_PAGE_SIZE);

    const tbody = d3.select("#data-table").select("tbody");
    const rows = tbody.selectAll("tr")
        .data(pageData)
        .join("tr")
        .attr("class", (d, i) => i % 2 === 1 ? "row-alt" : null);

    rows.selectAll("*").remove();

    rows.append("td")
        .attr("class", "cell-sales")
        .text(d => `$${d.sales.toLocaleString()}`);

    rows.append("td")
        .attr("class", d => `cell-profit ${d.profit >= 0 ? "positive" : "negative"}`)
        .text(d => `${d.profit}%`);

    const categoryCell = rows.append("td").attr("class", "cell-category");
    categoryCell.append("span")
        .attr("class", "category-dot")
        .style("background", d => CATEGORY_COLORS[d.category] || FALLBACK_COLOR);
    categoryCell.append("span").text(d => d.category);

    rows.append("td").text(d => d.sub_category);
    rows.append("td").text(d => d.product_name);

    renderTablePagination();
}

function renderTablePagination() {
    const { data, page } = tableState;
    const totalPages = Math.max(1, Math.ceil(data.length / TABLE_PAGE_SIZE));

    const container = d3.select("#table-pagination");
    container.selectAll("*").remove();

    if (data.length === 0) {
        container.style("display", "none");
        return;
    }
    container.style("display", "flex");

    container.append("span")
        .attr("class", "pagination-count")
        .text(`共 ${data.length} 筆`);

    container.append("button")
        .attr("class", "btn")
        .attr("type", "button")
        .text("上一頁")
        .property("disabled", page <= 1)
        .on("click", () => {
            tableState.page -= 1;
            renderTablePage();
        });

    container.append("span")
        .attr("class", "pagination-page")
        .text(`第 ${page} / ${totalPages} 頁`);

    container.append("button")
        .attr("class", "btn")
        .attr("type", "button")
        .text("下一頁")
        .property("disabled", page >= totalPages)
        .on("click", () => {
            tableState.page += 1;
            renderTablePage();
        });
}

function renderScatterLegend(data) {
    const legend = d3.select("#scatter_legend");
    legend.selectAll("*").remove();

    const present = new Set(data.map(d => d.category));
    const categories = CATEGORY_ORDER.filter(c => present.has(c));

    const item = legend.selectAll(".viz-legend-item")
        .data(categories)
        .join("div")
        .attr("class", "viz-legend-item");

    item.append("span")
        .attr("class", "viz-legend-swatch")
        .style("background", d => CATEGORY_COLORS[d]);

    item.append("span").text(d => d);
}

function createSubCategorySelect(subCategories) {
    const selectedInfoDiv = document.getElementById('selected-info');
    selectedInfoDiv.innerHTML = '';

    if (Array.isArray(subCategories)) {
        const select = document.createElement('select');
        select.id = 'subCategorySelect';

        const defaultOption = document.createElement('option');
        defaultOption.text = '-- 選擇 Sub Category --';
        defaultOption.value = '';
        select.appendChild(defaultOption);

        subCategories.forEach(sub => {
            const option = document.createElement('option');
            option.value = sub;
            option.textContent = sub;
            select.appendChild(option);
        });

        select.addEventListener('change', (event) => {
            const selected = event.target.value;

            // 篩選符合 sub_category 的資料（空值則用原始資料）
            const filteredData = selected
                ? originalData.filter(d => d.sub_category === selected)
                : originalData;

            drawScatterplot(filteredData); // 重畫圖
        });

        selectedInfoDiv.appendChild(select);
    } else {
        selectedInfoDiv.textContent = 'sub_category 資料格式錯誤';
    }
}
