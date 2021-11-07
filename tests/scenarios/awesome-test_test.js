const chai = require("chai");
const assert = chai.assert;

const { I } = inject();

Feature('API tests');

Scenario('Verify urls with GET method', async () => {
    const res = await I.sendGetRequest('/urls/');
    await assert.equal(res.status, 200);
});

Scenario('Verify queries with GET method', async () => {
    const res = await I.sendGetRequest('/search_queries/');
    await assert.equal(res.status, 200);
});

Scenario('Verify queries with GET method by setting query name', async () => {
    const res = await I.sendGetRequest('/search_queries/hello world');
    await assert.equal(res.status, 200);
});

Scenario('Verify queries with POST method', async () => {
    await I.setRequestTimeout(100000);
    headers = {
        "query": "npm"
    }
    const res = await I.sendPostRequest('/search_queries/', headers);
    await assert.equal(res.status, 200);
    await assert.equal(res.data.query, headers.query);
    const repetitious = await I.sendPostRequest('/search_queries/', headers);
    await assert.equal(repetitious.data.detail, 'Query already exist.');
    await I.sendDeleteRequest(`/search_queries/${res.data.id}`);
});

Scenario('Verify queries with DELETE method', async () => {
    await I.setRequestTimeout(100000);
    headers = {
        "query": "npm"
    }
    const res = await I.sendPostRequest('/search_queries/', headers);
    await assert.equal(res.status, 200);
    await assert.equal(res.data.query, headers.query);
    await I.sendDeleteRequest(`/search_queries/${res.data.id}`);
    const res_after_delete = await I.sendGetRequest(`/search_queries/${headers.query}`)
    await assert.equal(res_after_delete.data.detail, 'Query not found')
})
