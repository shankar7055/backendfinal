// Enhanced frontend script: handles data loading, theme toggle, nav and chat interactions
const API_BASE = window.location.origin + '/api';

document.addEventListener('DOMContentLoaded', () => {
    initUI();
    loadAll();
});

function initUI(){
    // Theme toggle
    const toggle = document.getElementById('toggleTheme');
    toggle.addEventListener('click', () => {
        document.body.classList.toggle('light-mode');
        const icon = toggle.querySelector('i');
        icon.classList.toggle('fa-sun');
        icon.classList.toggle('fa-moon');
        localStorage.setItem('theme', document.body.classList.contains('light-mode') ? 'light' : 'dark');
    });

    // Apply saved theme
    if(localStorage.getItem('theme') === 'light'){
        document.body.classList.add('light-mode');
        toggle.querySelector('i').classList.replace('fa-moon','fa-sun');
    }

    // Nav (visual only for now)
    document.querySelectorAll('.sidebar nav li').forEach(li => li.addEventListener('click', (e)=>{
        document.querySelectorAll('.sidebar nav li').forEach(x=>x.classList.remove('active'));
        li.classList.add('active');
        // Map nav to actions
        const txt = li.textContent.trim().toLowerCase();
        if(txt.includes('overview')){ loadOverview(); scrollToCard('overview-content'); }
        else if(txt.includes('finance')){ loadFinancialInsights(); scrollToCard('financial-content'); }
        else if(txt.includes('inventory')){ loadInventoryStatus(); scrollToCard('inventory-content'); }
        else if(txt.includes('customer')){ loadCustomerLoyalty(); scrollToCard('loyalty-content'); }
        else if(txt.includes('competitor')){ loadCompetitorAnalysis(); }
        else if(txt.includes('operation')){ alert('Operations panel: invoice generation and automation coming soon.'); }
    }));

    // Scrape and refresh buttons
    document.getElementById('scrapeBtn').addEventListener('click', async ()=>{
        const btn = document.getElementById('scrapeBtn');
        btn.disabled = true; btn.textContent = 'Scraping...';
        try{
            const res = await fetch(API_BASE.replace('/api','') + '/api/competitor/scrape');
            const data = await res.json();
            console.log('Scrape result', data);
            btn.textContent = 'Scraped';
            setTimeout(()=>btn.textContent='Scrape Competitors',1500);
        }catch(err){
            console.error(err); btn.textContent='Failed'; setTimeout(()=>btn.textContent='Scrape Competitors',1500);
        } finally { btn.disabled = false }
    });

    document.getElementById('refreshBtn').addEventListener('click', ()=> loadAll());

    // Chat input behavior
    const chatInput = document.getElementById('chat-query');
    chatInput.addEventListener('keypress', (e)=>{ if(e.key === 'Enter'){ sendMessage(); }});
}

function scrollToCard(id){
    const el = document.getElementById(id);
    if(!el) return;
    el.scrollIntoView({behavior:'smooth',block:'center'});
}

function loadAll(){
    loadOverview();
    loadFinancialInsights();
    loadInventoryStatus();
    loadCustomerLoyalty();
}

async function loadOverview(){
    const el = document.getElementById('overview-content');
    el.innerHTML = '<div class="loading">Loading overview...</div>';
    try{
        const resp = await fetch(`${API_BASE}/overview`);
        const data = await resp.json();
        if(data.error) return el.innerHTML = `<div class="loading">${data.error}</div>`;
        const metrics = data.metrics || {};
        // Use keys returned by backend (TotalRevenue, AverageDailyRevenue, TotalDaysTracked)
        el.innerHTML = `
            <div class="metric"><div class="metric-label">Total Revenue</div><div class="metric-value">₹${metrics.TotalRevenue||0}</div></div>
            <div class="metric"><div class="metric-label">Average Daily Revenue</div><div class="metric-value">₹${metrics.AverageDailyRevenue||0}</div></div>
            <div class="metric"><div class="metric-label">Last 7 Day Revenue</div><div class="metric-value">₹${metrics.Last7DayRevenue||0}</div></div>
        `;

        // Render chart if data present
        const chartData = (data.daily_sales_chart_data || []).map(r=>({date:r.date||r.date, revenue: r.revenue||r.revenue}));
        renderOverviewChart(chartData);
    }catch(e){ el.innerHTML = '<div class="loading">Failed to load overview</div>' }
}

function renderOverviewChart(points){
    try{
        const ctx = document.getElementById('overviewChart');
        if(!ctx) return;
        // Prepare labels and data
        const labels = points.map(p=> new Date(p.date).toLocaleDateString());
        const data = points.map(p=> Number(p.revenue || 0));
        if(window.__overviewChart){ window.__overviewChart.destroy(); }
        window.__overviewChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Daily Revenue',
                    data: data,
                    borderColor: 'rgba(61,162,255,0.95)',
                    backgroundColor: 'rgba(61,162,255,0.12)',
                    fill: true,
                    tension: 0.25,
                    pointRadius: 3
                }]
            },
            options: {plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{grid:{color:'rgba(255,255,255,0.03)'}}}
        });
    }catch(e){ console.warn('Chart render failed', e) }
}

function renderInventoryChart(series, product_id){
    try{
        const ctx = document.getElementById('inventoryChart');
        if(!ctx) return;
        const labels = series.map(p=> new Date(p.date).toLocaleDateString());
        const data = series.map(p=> Number(p.quantity || 0));
        if(window.__inventoryChart){ window.__inventoryChart.destroy(); }
        window.__inventoryChart = new Chart(ctx, {
            type: 'bar',
            data: { labels, datasets:[{label:`Sales - ${product_id}`, data, backgroundColor:'rgba(61,162,255,0.6)'}] },
            options:{plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{beginAtZero:true}}}
        });
    }catch(e){ console.warn('Inventory chart failed', e) }
}

function renderCustomersChart(customers){
    try{
        const ctx = document.getElementById('customersChart');
        if(!ctx) return;
        const labels = customers.map(c=> c.name);
        const data = customers.map(c=> Number(c.total_spent||0));
        if(window.__customersChart){ window.__customersChart.destroy(); }
        window.__customersChart = new Chart(ctx, {
            type: 'bar',
            data: { labels, datasets:[{label:'Top Customers', data, backgroundColor:'rgba(46,204,113,0.8)'}] },
            options:{plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{beginAtZero:true}}}
        });
    }catch(e){ console.warn('Customers chart failed', e) }
}

async function loadFinancialInsights(){
    const el = document.getElementById('financial-content');
    el.innerHTML = '<div class="loading">Loading financial insights...</div>';
    try{
        const resp = await fetch(`${API_BASE}/financials/insights`);
        const data = await resp.json();
        if(data.error) return el.innerHTML = `<div class="loading">${data.error}</div>`;
        const raw = data.raw_financial_data || data.financial_summary || {};
        const ai = data.ca_summary_report || data.ai_insights || '';
        el.innerHTML = `
            <div class="metric"><div class="metric-label">Revenue</div><div class="metric-value">₹${raw.TotalRevenue||0}</div></div>
            <div class="metric"><div class="metric-label">Net Profit</div><div class="metric-value">₹${raw.NetProfit||0}</div></div>
            <div style="margin-top:8px;color:var(--muted);white-space:pre-wrap">${ai}</div>
        `;
    }catch(e){ el.innerHTML = '<div class="loading">Failed to load financials</div>' }
}

async function loadInventoryStatus(){
    const el = document.getElementById('inventory-content');
    el.innerHTML = '<div class="loading">Loading inventory...</div>';
    try{
        const resp = await fetch(`${API_BASE}/inventory/automation`);
        const data = await resp.json();
        if(data.error) return el.innerHTML = `<div class="loading">${data.error}</div>`;
        const low = data.low_stock_report || [];
        if(!low.length){ el.innerHTML = '<div class="loading">All items are well stocked!</div>'; return }
        let html = '';
        low.forEach(i=>{
            html += `<div class="metric"><div class="metric-label">${i.name}</div><div style="text-align:right"><div style="font-weight:700">${i.current_stock} units</div><div style="color:var(--muted);font-size:12px">Reorder: ${i.recommendation_qty} • Threshold: ${i.dynamic_threshold}</div></div></div>`;
        });
        el.innerHTML = html;
        // Also load trend for first low-stock item or default product P001
        const first = (low[0] && low[0].product_id) ? low[0].product_id : 'P001';
        const trendResp = await fetch(`${API_BASE}/inventory/trends?product_id=${first}&days=30`);
        const trend = await trendResp.json();
        if(!trend.error){ renderInventoryChart(trend.series, first); }
    }catch(e){ el.innerHTML = '<div class="loading">Failed to load inventory</div>' }
}

async function loadCustomerLoyalty(){
    const el = document.getElementById('loyalty-content');
    el.innerHTML = '<div class="loading">Loading customers...</div>';
    try{
        const resp = await fetch(`${API_BASE}/customers/loyalty`);
        const data = await resp.json();
        if(data.error) return el.innerHTML = `<div class="loading">${data.error}</div>`;
        const customers = data.top_customers || [];
        let html = '';
        customers.slice(0,6).forEach(c=>{
            html += `<div class="metric"><div class="metric-label">${c.name}</div><div class="metric-value">₹${c.total_spent}</div></div>`;
        });
        el.innerHTML = html;
        // render customers chart
        renderCustomersChart(customers.slice(0,6));
    }catch(e){ el.innerHTML = '<div class="loading">Failed to load customers</div>' }
}

// Competitor analysis panel
async function loadCompetitorAnalysis(){
    showModal('<div class="loading">Loading competitor analysis...</div>');
    try{
        const resp = await fetch(`${API_BASE}/sku/market-analysis`);
        const data = await resp.json();
        if(data.error) return showModal(`<div class="loading">${data.error}</div>`);

        const market = data.product_market_data || {};
        const gen = data.pricing_recommendation || '';
        const computed = data.computed_recommendation || market.ComputedRecommendation || {};

        const html = `
            <h3>SKU Market Analysis - ${market.InternalProduct ? market.InternalProduct.name : 'P001'}</h3>
            <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:12px">
                <div style="flex:1;min-width:220px" class="metric"><div class="metric-label">Our Price</div><div class="metric-value">₹${market.InternalProduct ? market.InternalProduct.price : '-'}</div></div>
                <div style="flex:1;min-width:220px" class="metric"><div class="metric-label">Competitor Price</div><div class="metric-value">₹${market.ClosestCompetitor ? market.ClosestCompetitor.price : '-'}</div></div>
                <div style="flex:1;min-width:220px" class="metric"><div class="metric-label">Price Gap</div><div class="metric-value">₹${market.PriceGap || 0}</div></div>
            </div>
            <h4 style="margin-top:12px">Computed Recommendation</h4>
            <div style="color:var(--muted);white-space:pre-wrap">${computed.reason || JSON.stringify(computed)}</div>
            <h4 style="margin-top:12px">GenAI Advice</h4>
            <div style="color:var(--muted);white-space:pre-wrap">${gen}</div>
        `;
        showModal(html);
    }catch(e){ showModal('<div class="loading">Failed to load competitor analysis</div>') }
}

// Modal helpers
function showModal(innerHtml){
    const modal = document.getElementById('modal');
    const body = document.getElementById('modal-body');
    body.innerHTML = innerHtml;
    modal.style.display = 'flex';
    modal.querySelector('.modal-close').onclick = ()=> closeModal();
    modal.onclick = (e)=>{ if(e.target === modal) closeModal(); };
}
function closeModal(){ document.getElementById('modal').style.display = 'none'; document.getElementById('modal-body').innerHTML = ''; }

// Chat
async function sendMessage(){
    const qEl = document.getElementById('chat-query');
    const query = (qEl.value||'').trim();
    if(!query) return;
    addMessage(query,'user'); qEl.value='';
    try{
        const res = await fetch(window.location.origin + '/ai/chatbot',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({query})});
        const data = await res.json();
        if(data.error) addMessage('Error: '+data.error,'ai'); else addMessage(data.response,'ai');
    }catch(e){ addMessage('AI service unavailable','ai') }
}

function addMessage(text, sender){
    const area = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = `message ${sender}-message`;
    const time = new Date().toLocaleTimeString();
    div.innerHTML = `<div style="font-size:13px;color:var(--muted);margin-bottom:6px">${sender==='user'?'You':'Assistant'} • ${time}</div><div>${escapeHtml(text).replace(/\n/g,'<br>')}</div>`;
    area.appendChild(div);
    area.scrollTop = area.scrollHeight;
}

function escapeHtml(unsafe){ return unsafe.replace(/[&<>"']/g, function(m){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]}); }