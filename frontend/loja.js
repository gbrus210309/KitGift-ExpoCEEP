'use strict';
const $ = id => document.getElementById(id);
const money = new Intl.NumberFormat('pt-BR', {style:'currency',currency:'BRL'});
let items = [], loading = false, selectedId = null;
const normalize = value => String(value).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
function element(tag, text, cls) { const n=document.createElement(tag); n.textContent=text; if(cls)n.className=cls; return n; }
function fillDetail(p) {
  $('detail-title').textContent=p.nome;
  $('detail-category').textContent=p.categoria;
  $('detail-description').textContent=p.descricao || 'Mais informações sobre este kit em breve.';
  $('detail-price').textContent=money.format(p.preco/100);
  $('detail-stock').textContent=p.estoque>0 ? 'Disponível no catálogo' : 'Esgotado no momento';
}
function render() {
  let filtered=items.filter(p=>(!$('category').value || String(p.id_categoria)===$('category').value) && normalize(p.nome+' '+(p.descricao||'')+' '+p.categoria).includes(normalize($('search').value.trim())));
  const sort=$('sort').value;
  filtered.sort((a,b)=>sort==='low'?a.preco-b.preco:sort==='high'?b.preco-a.preco:sort==='name'?a.nome.localeCompare(b.nome,'pt-BR'):b.id_produto-a.id_produto);
  $('count').textContent=filtered.length+' kit'+(filtered.length===1?'':'s');
  $('grid').replaceChildren();
  if(!filtered.length) $('grid').append(element('p',items.length?'Nenhum kit encontrado. Experimente outra busca ou categoria.':'Novos kits estão a caminho. Volte em breve!'));
  for(const p of filtered) {
    const card=element('article','','kit'), visual=element('div','','visual');
    const fallback=()=>{ const t=element('div',p.categoria,'placeholder');t.append(element('small','KITGIFT · SELEÇÃO DE KITS'));visual.replaceChildren(t); };
    fallback();
    if(p.imagem) { try { const url=new URL(p.imagem,location.origin); if(['http:','https:'].includes(url.protocol)) {const img=new Image();img.alt=p.nome;img.loading='lazy';img.referrerPolicy='no-referrer';img.onload=()=>visual.replaceChildren(img);img.onerror=fallback;img.src=url.href;} }catch{} }
    const bottom=element('div','','card-bottom'), button=element('button','Conhecer o kit ↗','details-button');button.type='button';button.setAttribute('aria-label','Conhecer '+p.nome);
    button.onclick=()=>{selectedId=p.id_produto;fillDetail(p);$('detail').showModal();};
    bottom.append(element('span',money.format(p.preco/100),'price'),button);
    card.append(visual,element('p',p.categoria,'category'),element('h3',p.nome),element('p',p.descricao||'Um conjunto pensado para facilitar sua escolha.','description'),bottom,element('p',p.estoque>0?'Disponível':'Esgotado no momento','availability'));
    $('grid').append(card);
  }
}
async function refresh() {
  if(loading)return;loading=true;$('reload').disabled=true;
  try {
    const response=await fetch('/api/catalogo',{cache:'no-store',signal:AbortSignal.timeout(10000)});
    if(!response.ok)throw Error();
    const data=await response.json();if(!Array.isArray(data))throw Error();items=data;
    const current=$('category').value, cats=new Map(items.map(p=>[String(p.id_categoria),p.categoria]));
    $('category').replaceChildren(new Option('Todas as categorias',''));
    [...cats].sort((a,b)=>a[1].localeCompare(b[1],'pt-BR')).forEach(([id,name])=>$('category').add(new Option(name,id)));
    $('category').value=cats.has(current)?current:'';
    $('status').textContent='';$('status').className='';render();
    if($('detail').open){const p=items.find(p=>p.id_produto===selectedId);if(p)fillDetail(p);else $('detail').close();}
  }catch { $('status').textContent='Não foi possível atualizar o catálogo. Tente novamente em Atualizar catálogo.'+(items.length?' Os kits exibidos podem estar desatualizados.':'');$('status').className='error'; }
  finally{loading=false;$('reload').disabled=false;}
}
$('search').addEventListener('input',render);$('category').addEventListener('change',render);$('sort').addEventListener('change',render);$('reload').addEventListener('click',refresh);$('close-detail').onclick=()=>$('detail').close();
document.addEventListener('visibilitychange',()=>{if(!document.hidden)refresh();});
setInterval(()=>{if(!document.hidden)refresh();},15000);
refresh();
