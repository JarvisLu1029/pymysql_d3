function drawScatterplot(data) {
    const svg = d3.select("#scatter_plot"),
        width = +svg.attr("width"),
        height = +svg.attr("height"),
        margin = { top: 20, right: 30, bottom: 30, left: 40 };

    svg.selectAll("*").remove();

    // 示範資料
    // const data = [
    //     { x: 10, y: 20, category: "A" },
    //     { x: 30, y: 40, category: "B" },
    //     { x: 50, y: 60, category: "C" },
    //     { x: 70, y: 80, category: "D" },
    //     { x: 50, y: 90, category: "C" },
    //     { x: 90, y: 100, category: "E" }
    // ];

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

    const color = d3.scaleOrdinal().domain(data.map(d => d.category)).range(d3.schemeCategory10);

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

    const brush = d3.brush()
        .extent([[margin.left, margin.top], [width - margin.right, height - margin.bottom]])
        .on("brush end", brushed);

    svg.append("g")
        .attr("class", "brush")
        .call(brush);

    function brushed({ selection }) {
        const tbody = d3.select("#data-table").select("tbody");
        tbody.selectAll("tr").remove();

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

        tbody.selectAll("tr")
            .data(selectedData)
            .enter()
            .append("tr")
            .html(d => `<td>${d.sales}</td><td>${d.profit}</td><td>${d.category}</td><td>${d.sub_category}</td><td>${d.product_name}</td>`);
    }
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