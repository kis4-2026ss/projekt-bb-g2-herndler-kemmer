'use strict';

import {dataManagerInstance} from "./datamanager.js";

window.onload = function () {

    const form = document.getElementById("prompForm");
    const input = document.getElementById("queryInput");
    const submitQueryButton = document.getElementById("submitQuery");
    const responseText = document.getElementById("responseText");
    const usedQueryText = document.getElementById("usedSqlQuery");
    const usedSqlQueryContainer = document.getElementById("usedSqlQueryContainer");
    const rawResultsContainer = document.getElementById("rawResultsContainer");
    const tableHeader = document.getElementById("tableHeader");
    const tableBody = document.getElementById("tableBody");
    const submitButton = document.getElementById("submitQuery");
    const loadingSpinner = document.getElementById("loadingSpinner");
    const cancelQueryButton = document.getElementById("cancelQuery");

    function showLoading() {
        loadingSpinner.style.display = "block";
        cancelQueryButton.style.display = "block";
        submitButton.disabled = true;
        input.disabled = true;
    }

    function hideLoading() {
        loadingSpinner.style.display = "none";
        cancelQueryButton.style.display = "none";
        submitButton.disabled = false;
        input.disabled = false;
    }

    function formatSqlQuery(sql) {
        // Format SQL query with line breaks for readability
        return sql
            .replace(/\bSELECT\b/gi, "\nSELECT")
            .replace(/\bFROM\b/gi, "\nFROM")
            .replace(/\bWHERE\b/gi, "\nWHERE")
            .replace(/\bJOIN\b/gi, "\nJOIN")
            .replace(/\bLEFT\b/gi, "\nLEFT")
            .replace(/\bRIGHT\b/gi, "\nRIGHT")
            .replace(/\bINNER\b/gi, "\nINNER")
            .replace(/\bLIMIT\b/gi, "\nLIMIT")
            .replace(/\bORDER\s+BY\b/gi, "\nORDER BY")
            .replace(/\bGROUP\s+BY\b/gi, "\nGROUP BY")
            .trim();
    }

    function populateTable(data, columns) {
        if (!data || data.length === 0) {
            rawResultsContainer.style.display = "none";
            return;
        }

        // Clear existing table content
        tableHeader.innerHTML = "";
        tableBody.innerHTML = "";

        // Create header row
        columns.forEach(col => {
            const th = document.createElement("th");
            th.textContent = col;
            tableHeader.appendChild(th);
        });

        // Create data rows
        data.forEach(row => {
            const tr = document.createElement("tr");
            row.forEach(cell => {
                const td = document.createElement("td");
                td.textContent = cell;
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        });

        rawResultsContainer.style.display = "block";
    }

    function extractColumnsFromSQL(sql) {
        // Extract column names from SELECT clause
        const selectMatch = sql.match(/SELECT\s+(.*?)\s+FROM/i);
        if (selectMatch) {
            const selectClause = selectMatch[1];
            return selectClause.split(',').map(col => col.trim());
        }
        return [];
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const prompt = input.value;
        if (!prompt.trim()) return;

        if(!dataManagerInstance.isReady()) {
            return;
        }

        try {
            showLoading();

            const response = await dataManagerInstance.promptRequest(prompt);
            const answer = response.answer;
            const sqlContent = response.sql_query;

            responseText.textContent = answer;
            responseText.classList.remove("text-danger");
            responseText.style.whiteSpace = "pre-wrap";

            if (sqlContent) {
                usedSqlQueryContainer.style.display = "block";
                usedQueryText.innerHTML = formatSqlQuery(sqlContent).replace(/\n/g, "<br>");
            } else {
                usedSqlQueryContainer.style.display = "none";
            }

            // Populate raw results table
            if (response.raw_result && Array.isArray(response.raw_result)) {
                const columns = extractColumnsFromSQL(sqlContent);
                populateTable(response.raw_result, columns);
            } else {
                rawResultsContainer.style.display = "none";
            }

        } catch (error) {
            responseText.textContent = "Error: " + error.message;
            responseText.classList.add("text-danger");
            usedQueryText.textContent = "";
            rawResultsContainer.style.display = "none";
        } finally {
            hideLoading();
        }
    });

    // Shift+Enter to submit form
    input.addEventListener("keydown", (event) => {
        if (event.shiftKey && event.key === "Enter") {
            event.preventDefault();
            submitButton.click();
        }
    });

    cancelQueryButton.addEventListener("click", (ev) => {
        ev.stopPropagation();
        ev.preventDefault();
        dataManagerInstance.cancelRequest();
    });
};