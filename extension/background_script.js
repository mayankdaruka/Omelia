let rule = {
   conditions: [
      new chrome.declarativeContent.PageStateMatcher({
         pageUrl: { hostEquals: 'www.google.com', schemes: ['http', 'https'] }
      })
   ],
   actions: [ new chrome.declarativeContent.ShowPageAction() ]
}

chrome.runtime.onInstalled.addListener(() => {
   // chrome.storage.sync.set({ color: "#3aa757" }, () => console.log("The color is green."))
   chrome.declarativeContent.onPageChanged.removeRules(undefined, () => {
      chrome.declarativeContent.onPageChanged.addRules([rule])
   })
})

// chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {

//    // since only one tab should be active and in the current window at once
//    // the return variable should only have one entry
//    var activeTab = tabs[0];
//    var activeTabId = activeTab.id; // or do whatever you need
//    chrome.storage.sync.set({ curr_tab: activeTabId.url }, () => console.log("done"))
// });