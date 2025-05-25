function renderPieChart(data, selector = "#pie_chart", onClickHandler = null) {
    const pie_width = 500;
    const pie_height = 350;
    const radius = Math.min(pie_width, pie_height) / 2;

    // 清除舊圖
    d3.select(selector).selectAll("*").remove();

    const color = d3.scaleOrdinal()
        .domain(data.map(d => d.name))
        .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), data.length).reverse());

    const pie = d3.pie()
        .sort(null)
        .value(d => d.value);

    const arc = d3.arc()
        .innerRadius(0)
        .outerRadius(radius - 10);

    const labelRadius = radius * 0.8;
    const arcLabel = d3.arc()
        .innerRadius(labelRadius)
        .outerRadius(labelRadius);

    const arcs = pie(data);
    const svg = d3.select(selector)
        .append("svg")
        .attr("width", pie_width)
        .attr("height", pie_height)
        .attr("viewBox", [-pie_width / 2, -pie_height / 2, pie_width, pie_height])
        .attr("style", "max-width: 100%; height: auto; font: 14px sans-serif;");

    const tooltip = d3.select("#pie_chart_tooltip");

    svg.append("g")
        .attr("stroke", "white")
        .selectAll("path")
        .data(arcs)
        .join("path")
        .attr("fill", d => color(d.data.label))
        .attr("d", arc)
        .attr("cursor", "pointer")
        .on("click", (event, d) => {
            if (typeof onClickHandler === "function") {
                onClickHandler(d.data.label);
            }
        })
        .on("mouseover", function (event, d) {
            const total = d3.sum(data.map(d => d.value));
            const percent = (d.data.value / total) * 100;
            tooltip
                .style("visibility", "visible")
                .html(`<strong>${d.data.label}</strong>: ${percent.toFixed(1)}% (${d.data.value})`);

            d3.select(this)
                .transition()
                .duration(150)
                .attr("transform", "scale(1.02)")
                .attr("stroke", "#000")
                .attr("stroke-width", 1.5);
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
                .attr("transform", "scale(1)")
                .attr("stroke", "white")
                .attr("stroke-width", 1);
        });

    svg.append("g")
        .attr("text-anchor", "middle")
        .selectAll("text")
        .data(arcs)
        .join("text")
        .attr("transform", d => `translate(${arcLabel.centroid(d)})`)
        .call(text => text.append("tspan")
            .attr("y", "-0.4em")
            .attr("font-weight", "bold")
            .text(d => d.data.label))
        .call(text => {
            const total = d3.sum(data.map(d => d.value));
            text.filter(d => (d.endAngle - d.startAngle) > 0.25).append("tspan")
                .attr("x", 0)
                .attr("y", "0.7em")
                .attr("font-weight", "bold")
                .text(d => {
                    const percent = (d.data.value / total) * 100;
                    return `${percent.toFixed(1)}% (${d.data.value})`;
                });
        });
}
