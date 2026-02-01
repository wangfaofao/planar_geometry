// 加载 MathJax 库
var script = document.createElement('script');
script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
script.async = true;
document.head.appendChild(script);

// 配置 MathJax
window.MathJax = {
  tex: {
    inlineMath: [['\\(', '\\)']],
    displayMath: [['\\[', '\\]']]
  },
  svg: {
    fontCache: 'global'
  },
  startup: {
    pageReady: () => {
      // 在 MathJax 加载后处理 .math 标签
      handleMathSpans();
      return MathJax.typesetPromise();
    }
  }
};

// 处理 Sphinx 生成的 .math class 标签
function handleMathSpans() {
  const mathElements = document.querySelectorAll('span.math');
  
  mathElements.forEach(function(element) {
    // 获取文本内容
    const mathText = element.textContent;
    
    // 清除内容
    element.innerHTML = '';
    
    // 创建新的 script 标签用于 MathJax 处理
    const script = document.createElement('script');
    script.type = 'math/tex';
    script.textContent = mathText;
    element.appendChild(script);
  });
}

// 在文档加载完成后处理 .math 标签
document.addEventListener('DOMContentLoaded', function() {
  // 如果 MathJax 还未完全加载，等待一下再处理
  if (window.MathJax) {
    handleMathSpans();
    MathJax.typesetPromise().catch(err => console.log('MathJax error:', err));
  } else {
    // 延迟处理，确保 MathJax 已加载
    setTimeout(function() {
      handleMathSpans();
      if (window.MathJax) {
        MathJax.typesetPromise().catch(err => console.log('MathJax error:', err));
      }
    }, 1000);
  }
});
