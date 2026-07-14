function createFloatingWidget() {
  if (document.getElementById('survey-autofill-widget')) return;

  const widget = document.createElement('div');
  widget.id = 'survey-autofill-widget';
  widget.innerHTML = [
    '<div style="padding: 12px; background: #0f172a; color: white; border-radius: 8px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); font-family: system-ui, sans-serif; display: flex; flex-direction: column; gap: 10px; border: 1px solid #334155;">',
    '  <h3 style="margin: 0; font-size: 15px; text-align: center; color: #f8fafc;">Survey Auto-Filler</h3>',
    '  <button id="fill-all-tabs" style="padding: 8px 16px; background: #8b5cf6; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold;">Auto-Fill All Tabs (Mix 60-100%)</button>',
    '  <button id="fill-excellent" style="padding: 8px 16px; background: #3b82f6; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold;">Fill Current Tab (100%)</button>',
    '</div>'
  ].join('');
  
  widget.style.position = 'fixed';
  widget.style.bottom = '30px';
  widget.style.right = '30px';
  widget.style.zIndex = '9999999';

  document.body.appendChild(widget);

  document.getElementById('fill-all-tabs').addEventListener('click', () => autoFillAllTabs(-1));
  document.getElementById('fill-excellent').addEventListener('click', () => { fillSurveyOptions(0); clickSave(); });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


async function handlePopupsAggressive() {
    let popupCount = 0;
    
    // Wait max 3.5 seconds total for popups to appear
    for (let c = 0; c < 35; c++) { 
        await sleep(100);
        const popupOk = document.getElementById('popup_ok') || document.querySelector('input[value="موافق"], button.confirm');
        
        if (popupOk && popupOk.offsetParent !== null) {
            popupOk.click();
            popupCount++;
            
            // Wait for this specific popup to disappear before looking for the next one
            for(let d = 0; d < 10; d++) {
                await sleep(100);
                if (!document.getElementById('popup_ok') || document.getElementById('popup_ok') !== popupOk) {
                    break;
                }
            }
            
            if (popupCount >= 2) break; // Reached the 'Data Saved' popup
        }
    }
}

async function autoFillAllTabs(strategy) {
  const tabs = Array.from(document.querySelectorAll('.tablinks'));
  if (tabs.length === 0) {
      showToast("No tabs found! Make sure a subject is loaded.");
      return;
  }
  
  for (let i = 0; i < tabs.length; i++) {
    const tab = tabs[i];
    tab.click();
    
    // Wait for questions to load (fast polling)
    let checks = 0;
    let activeContent = null;
    let noSurvey = false;
    while (checks < 20) { // Max 3 seconds
        await sleep(150);
        activeContent = getActiveTabContent();
        if (activeContent) {
            if (activeContent.querySelectorAll('input[type="radio"]').length > 0) {
                break;
            }
            if (activeContent.innerText && activeContent.innerText.includes('لا يوجد استبيان')) {
                noSurvey = true;
                break;
            }
        }
        checks++;
    }
    
    if (noSurvey) {
        console.log("Tab " + (i+1) + " has no survey (لا يوجد استبيان). Skipping.");
        continue;
    }
    
    await sleep(150); // Tiny rendering buffer
    activeContent = getActiveTabContent();
    if (!activeContent) continue;
    
    // CHECK IF ALREADY FILLED
    const rows = activeContent.querySelectorAll('tr.element');
    if (rows.length > 0) {
        let checkedCount = 0;
        rows.forEach(row => {
            if (row.querySelector('input[type="radio"]:checked')) checkedCount++;
        });
        
        // If all rows (or all minus 1) are checked, skip entirely!
        if (checkedCount >= rows.length - 1) {
            console.log("Tab " + (i+1) + " already filled. Skipping.");
            continue; 
        }
    }
    
    fillSurveyOptions(strategy);
    clickSave();
    
    // Handle the popups aggressively and dynamically
    await handlePopupsAggressive();
  }
  
  showToast("Finished all tabs for this subject!", 4000);
}

function getActiveTabContent() {
    return Array.from(document.querySelectorAll('.tabcontent')).find(el => getComputedStyle(el).display === 'block');
}

function fillSurveyOptions(strategy) {
  const activeContent = getActiveTabContent() || document;
  const rows = activeContent.querySelectorAll('tr.element');
  
  rows.forEach(row => {
    const radio100 = row.querySelector('input[type="radio"][id^="100-"]');
    const radio80 = row.querySelector('input[type="radio"][id^="80-"]');
    const radio60 = row.querySelector('input[type="radio"][id^="60-"]');
    
    if (radio100 && radio80 && radio60) {
      let targetRadio = radio100;
      if (strategy === -1) {
          const rand = Math.random();
          if (rand < 0.33) targetRadio = radio60;
          else if (rand < 0.66) targetRadio = radio80;
          else targetRadio = radio100;
      }
      targetRadio.click();
      targetRadio.checked = true;
    } else {
      const radios = row.querySelectorAll('input[type="radio"]');
      if (radios.length >= 5) {
        let targetIndex = 0;
        if (strategy === -1) {
            const rand = Math.random();
            if (rand < 0.33) targetIndex = 2; // 60
            else if (rand < 0.66) targetIndex = 1; // 80
            else targetIndex = 0; // 100
        }
        if (radios[targetIndex]) {
            radios[targetIndex].click();
            radios[targetIndex].checked = true;
        }
      }
    }
  });

  const commentText = activeContent.querySelector('#CommentText') || document.getElementById('CommentText');
  if (commentText && !commentText.value) {
      commentText.value = "لا توجد تعليقات إضافية. شكراً لكم.";
      commentText.dispatchEvent(new Event('input', { bubbles: true }));
  }
}

function clickSave() {
  const activeContent = getActiveTabContent() || document;
  const saveBtn = activeContent.querySelector('button[id*="Save"], input[id*="Save"], img[src*="Save"]') || document.getElementById('SaveQuestionnaire');
  
  if (saveBtn) {
    const btnToClick = saveBtn.tagName === 'IMG' ? saveBtn.parentElement : saveBtn;
    btnToClick.click();
    btnToClick.style.outline = '4px solid #10b981';
  } else {
    console.log("Save button not found!");
  }
}

function showToast(msg, duration = 3000) {
  let toast = document.getElementById('survey-toast');
  if (!toast) {
      toast = document.createElement('div');
      toast.id = 'survey-toast';
      document.body.appendChild(toast);
  }
  toast.innerText = msg;
  toast.style.position = 'fixed';
  toast.style.bottom = '200px';
  toast.style.right = '30px';
  toast.style.background = '#10b981';
  toast.style.color = 'white';
  toast.style.padding = '12px 20px';
  toast.style.borderRadius = '6px';
  toast.style.zIndex = '9999999';
  toast.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
  toast.style.fontWeight = 'bold';
  toast.style.transition = 'opacity 0.5s';
  toast.style.opacity = '1';
  
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
    }, 500);
  }, duration);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', createFloatingWidget);
} else {
  createFloatingWidget();
}
