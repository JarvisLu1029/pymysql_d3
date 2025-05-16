function drawScatterplot(data) {
    const svg = d3.select("#scatter_plot"),
        width = +svg.attr("width"),
        height = +svg.attr("height"),
        margin = { top: 20, right: 30, bottom: 30, left: 40 };

    // 假設 data 是一個陣列，每個元素都有 x 和 y 屬性
    const xExtent = d3.extent(data, d => d.sales); // [minX, maxX]
    const yExtent = d3.extent(data, d => d.profit); // [minY, maxY]


    const x = d3.scaleLinear()
        .domain(xExtent)
        .range([margin.left, width - margin.right]);

    const y = d3.scaleLinear()
        .domain(yExtent)
        .range([height - margin.bottom, margin.top]);


    // 示範資料
    // const data = [
    //     { x: 10, y: 20, category: "A" },
    //     { x: 30, y: 40, category: "B" },
    //     { x: 50, y: 60, category: "C" },
    //     { x: 70, y: 80, category: "D" },
    //     { x: 50, y: 90, category: "C" },
    //     { x: 90, y: 100, category: "E" }
    // ];

    const color = d3.scaleOrdinal().domain(data.map(d => d.category)).range(d3.schemeCategory10);

    // 畫 X/Y 軸
    svg.append("g")
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x));

    svg.append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y));

    const dots = svg.append("g")
        .attr("stroke-width", 1.5)
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        .selectAll("circle")
        .data(data)
        .join("circle")
        .attr("cx", d => x(d.sales))
        .attr("cy", d => y(d.profit))
        .attr("fill", d => color(d.category))
        .attr("stroke", "#333")
        .attr("r", 3);

    // 定義 Brush
    const brush = d3.brush()
        .extent([[margin.left, margin.top], [width - margin.right, height - margin.bottom]])
        .on("brush end", brushed);

    svg.append("g")
        .attr("class", "brush")
        .call(brush);

    function brushed({ selection }) {
        const tbody = d3.select("#data-table").select("tbody");
        tbody.selectAll("tr").remove(); // 清空舊資料

        if (!selection) {
            dots.classed("selected", false);
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

        // 插入選取的資料到表格
        tbody.selectAll("tr")
            .data(selectedData)
            .enter()
            .append("tr")
            .html(d => `<td>${d.sales}</td><td>${d.profit}</td><td>${d.category}</td><td>${d.sub_category}</td><td>${d.product_name}</td>`);
    }
}
