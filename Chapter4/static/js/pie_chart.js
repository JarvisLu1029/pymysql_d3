const CATEGORICAL_COLORS = [
    "#2a78d6", // blue
    "#1baf7a", // aqua
    "#eda100", // yellow
    "#008300", // green
    "#4a3aa7", // violet
    "#e34948", // red
    "#e87ba4", // magenta
    "#eb6834", // orange
];

// 淺色（亮度較高）色塊用深色文字，其餘用白色文字，確保標籤對比足夠
function labelColorFor(hex) {
    const rgb = d3.color(hex).rgb();
    const luminance = (0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b) / 255;
    return luminance > 0.6 ? "#0b0b0b" : "#ffffff";
}

// 類別色板最多支援 8 種身分色；超過時將較小的項目合併為「其他」，
// 避免顏色重複或需要無止盡地產生新色相
function foldIntoOther(data, maxSlices = 8) {
    if (data.length <= maxSlices) return data;

    const sorted = [...data].sort((a, b) => b.value - a.value);
    const kept = sorted.slice(0, maxSlices - 1);
    const rest = sorted.slice(maxSlices - 1);
    const otherValue = d3.sum(rest, d => d.value);

    return [...kept, { label: "其他", value: otherValue }];
}

function renderPieChart(rawData, selector = "#pie_chart", onClickHandler = null) {
    const pie_width = 420;
    const pie_height = 340;
    const radius = Math.min(pie_width, pie_height) / 2;

    const data = foldIntoOther(rawData);

    // 清除舊圖
    d3.select(selector).selectAll("*").remove();

    const color = d3.scaleOrdinal()
        .domain(data.map(d => d.label))
        .range(CATEGORICAL_COLORS);

    const pie = d3.pie()
        .sort(null)
        .value(d => d.value);

    const arc = d3.arc()
        .innerRadius(radius * 0.55) // 甜甜圈造型，中心留白讓標籤更清爽
        .outerRadius(radius - 10)
        .cornerRadius(2);

    const labelRadius = (radius * 0.55 + radius - 10) / 2;
    const arcLabel = d3.arc()
        .innerRadius(labelRadius)
        .outerRadius(labelRadius);

    const arcs = pie(data);
    const svg = d3.select(selector)
        .append("svg")
        .attr("width", pie_width)
        .attr("height", pie_height)
        .attr("viewBox", [-pie_width / 2, -pie_height / 2, pie_width, pie_height])
        .attr("style", "max-width: 100%; height: auto; font-family: system-ui, -apple-system, 'Segoe UI', 'PingFang TC', 'Microsoft JhengHei', sans-serif; font-size: 12px;");

    const tooltip = d3.select("#pie_chart_tooltip");
    const total = d3.sum(data, d => d.value);

    svg.append("g")
        .attr("stroke", "#fcfcfb")
        .attr("stroke-width", 2)
        .selectAll("path")
        .data(arcs)
        .join("path")
        .attr("fill", d => color(d.data.label))
        .attr("d", arc)
        .attr("cursor", () => typeof onClickHandler === "function" ? "pointer" : "default")
        .on("click", (event, d) => {
            if (typeof onClickHandler === "function" && d.data.label !== "其他") {
                onClickHandler(d.data.label);
            }
        })
        .on("mouseover", function (event, d) {
            const percent = (d.data.value / total) * 100;
            tooltip
                .style("visibility", "visible")
                .html(`<strong>${d.data.label}</strong><br>${percent.toFixed(1)}% (${d.data.value.toLocaleString()})`);

            d3.select(this)
                .transition()
                .duration(150)
                .attr("transform", "scale(1.03)");
        })
        .on("mousemove", function (event) {
            tooltip
                .style("top", (event.pageY - 30) + "px")
                .style("left", (event.pageX + 10) + "px");
        })
        .on("mouseout", function () {
            tooltip.style("visibility", "hidden");

            d3.select(this)
                .transition()
                .duration(150)
                .attr("transform", "scale(1)");
        });

    svg.append("g")
        .attr("text-anchor", "middle")
        .selectAll("text")
        .data(arcs)
        .join("text")
        .attr("fill", d => labelColorFor(color(d.data.label)))
        .attr("transform", d => `translate(${arcLabel.centroid(d)})`)
        .style("pointer-events", "none")
        .call(text => text.filter(d => (d.endAngle - d.startAngle) > 0.2).append("tspan")
            .attr("y", "-0.3em")
            .attr("font-weight", "600")
            .text(d => d.data.label))
        .call(text => {
            text.filter(d => (d.endAngle - d.startAngle) > 0.2).append("tspan")
                .attr("x", 0)
                .attr("y", "0.9em")
                .text(d => {
                    const percent = (d.data.value / total) * 100;
                    return `${percent.toFixed(1)}%`;
                });
        });

    // 中心顯示總數，呼應甜甜圈留白
    svg.append("text")
        .attr("text-anchor", "middle")
        .attr("y", "-0.2em")
        .attr("fill", "#0b0b0b")
        .attr("font-size", 20)
        .attr("font-weight", 600)
        .text(total.toLocaleString());

    svg.append("text")
        .attr("text-anchor", "middle")
        .attr("y", "1.3em")
        .attr("fill", "#898781")
        .attr("font-size", 11)
        .text("總訂單數");
}
