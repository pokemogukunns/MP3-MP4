const puppeteer = require('puppeteer');
const JSZip = require('jszip');
const fs = require('fs');
const axios = require('axios');
const path = require('path');
const process = require('process');

// コマンドライン引数からURLとZIPファイル名を取得
const [,, pageUrl, zipFileName] = process.argv;

if (!pageUrl) {
    console.error('Usage: node savePageToZip.js <pageUrl> [zipFileName]');
    process.exit(1);
}

async function fetchPageResources(url, zip, basePath) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    await page.goto(url, { waitUntil: 'networkidle2' });

    // ページのHTMLを取得してZIPに追加
    const pageContent = await page.content();
    zip.file('index.html', pageContent);

    // ページ内のリソースを取得
    const resources = await page.evaluate(() => {
        const resources = [];
        const addResource = (url, type) => {
            if (url && !resources.includes(url)) {
                resources.push({ url, type });
            }
        };

        // CSSファイル
        document.querySelectorAll('link[rel="stylesheet"]').forEach(link => addResource(link.href, 'css'));

        // JavaScriptファイル
        document.querySelectorAll('script[src]').forEach(script => addResource(script.src, 'js'));

        // 画像ファイル
        document.querySelectorAll('img[src]').forEach(img => addResource(img.src, 'img'));

        // 動画ファイル
        document.querySelectorAll('video source[src]').forEach(video => addResource(video.src, 'video'));

        return resources;
    });

    // リソースをZIPに追加
    for (const resource of resources) {
        const url = new URL(resource.url, url).href;
        const filePath = path.join(basePath, resource.type, path.basename(new URL(resource.url).pathname));

        try {
            const response = await axios.get(url, { responseType: 'arraybuffer' });
            zip.file(filePath, response.data);
        } catch (error) {
            console.error(`Failed to fetch resource ${url}: ${error.message}`);
        }
    }

    await browser.close();
}

async function saveZipFile(url, zipFileName) {
    const zip = new JSZip();

    // リソースを収集してZIPに追加
    await fetchPageResources(url, zip, '');

    // ZIPファイルを生成して保存
    zip.generateAsync({ type: 'nodebuffer' })
        .then(content => fs.writeFileSync(`${zipFileName}.zip`, content))
        .catch(err => console.error('Error generating ZIP file:', err));
}

// URLとZIPファイル名を指定して保存
saveZipFile(pageUrl, zipFileName || 'downloaded_page')
    .then(() => console.log('Page and resources have been saved to ZIP file'))
    .catch(err => console.error('Error saving page to ZIP file:', err));
