import { useState } from 'react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../components/ui/select';
import { Loader2, Sparkles, Download, Eye } from 'lucide-react';
import { mockLanguages, mockTrafficSources, mockTargetActions } from '../mock';

const Home = () => {
  const [formData, setFormData] = useState({
    theme: '',
    language: '',
    trafficSource: '',
    targetAction: ''
  });
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedLanding, setGeneratedLanding] = useState(null);

  const handleGenerate = async () => {
    if (!formData.theme || !formData.language || !formData.trafficSource || !formData.targetAction) {
      alert('Пожалуйста, заполните все поля');
      return;
    }

    setIsGenerating(true);
    
    // Simulate generation with mock data
    setTimeout(() => {
      const mockResult = {
        id: Date.now().toString(),
        ...formData,
        createdAt: new Date().toISOString(),
        html: generateMockHTML(formData),
        lighthouse: Math.floor(Math.random() * 5) + 96
      };
      setGeneratedLanding(mockResult);
      setIsGenerating(false);
    }, 3000);
  };

  const generateMockHTML = (data) => {
    return `<!DOCTYPE html>
<html lang="${data.language === 'Русский' ? 'ru' : 'en'}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${data.theme}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
        .hero { min-height: 100vh; display: flex; align-items: center; justify-content: center; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center; padding: 2rem; }
        h1 { font-size: 3rem; margin-bottom: 1rem; }
        p { font-size: 1.5rem; margin-bottom: 2rem; }
        button { background: white; color: #667eea; padding: 1rem 3rem; border: none; 
                 border-radius: 50px; font-size: 1.2rem; cursor: pointer; font-weight: 600; }
    </style>
</head>
<body>
    <div class="hero">
        <div>
            <h1>${data.theme}</h1>
            <p>Созданный с AI технологией</p>
            <button>${data.targetAction}</button>
        </div>
    </div>
</body>
</html>`;
  };

  const handleDownload = (format) => {
    if (!generatedLanding) return;
    
    const blob = new Blob([generatedLanding.html], { type: 'text/html' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `landing-${generatedLanding.id}.${format}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const handlePreview = () => {
    if (!generatedLanding) return;
    
    const previewWindow = window.open('', '_blank');
    previewWindow.document.write(generatedLanding.html);
    previewWindow.document.close();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-violet-600 to-indigo-600 rounded-lg flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">
              LandingGen AI
            </h1>
          </div>
          <div className="text-sm text-slate-600">
            Генератор посадочных страниц уровня Awwwards
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h2 className="text-5xl font-bold mb-4 bg-gradient-to-r from-violet-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
              Создайте идеальный Landing Page за минуты
            </h2>
            <p className="text-xl text-slate-600 max-w-2xl mx-auto">
              AI-генерация эпических посадочных страниц с автоматическим прохождением модерации Google Ads. 
              Lighthouse 100/100. Глобальный комплаенс.
            </p>
          </div>

          {/* Generation Form */}
          <div className="bg-white rounded-2xl shadow-xl border border-slate-200 p-8 mb-8">
            <h3 className="text-2xl font-semibold mb-6 text-slate-800">Параметры генерации</h3>
            
            <div className="space-y-6">
              {/* Theme */}
              <div>
                <Label htmlFor="theme" className="text-base font-medium mb-2 block">
                  Тема landing page
                </Label>
                <Input
                  id="theme"
                  placeholder="Например: Онлайн школа программирования"
                  value={formData.theme}
                  onChange={(e) => setFormData({ ...formData, theme: e.target.value })}
                  className="h-12 text-base"
                />
              </div>

              {/* Language */}
              <div>
                <Label htmlFor="language" className="text-base font-medium mb-2 block">
                  Язык
                </Label>
                <Select
                  value={formData.language}
                  onValueChange={(value) => setFormData({ ...formData, language: value })}
                >
                  <SelectTrigger className="h-12 text-base">
                    <SelectValue placeholder="Выберите язык" />
                  </SelectTrigger>
                  <SelectContent>
                    {mockLanguages.map((lang) => (
                      <SelectItem key={lang} value={lang}>
                        {lang}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Traffic Source */}
              <div>
                <Label htmlFor="traffic" className="text-base font-medium mb-2 block">
                  Источник трафика
                </Label>
                <Select
                  value={formData.trafficSource}
                  onValueChange={(value) => setFormData({ ...formData, trafficSource: value })}
                >
                  <SelectTrigger className="h-12 text-base">
                    <SelectValue placeholder="Выберите источник" />
                  </SelectTrigger>
                  <SelectContent>
                    {mockTrafficSources.map((source) => (
                      <SelectItem key={source} value={source}>
                        {source}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Target Action */}
              <div>
                <Label htmlFor="action" className="text-base font-medium mb-2 block">
                  Целевое действие
                </Label>
                <Select
                  value={formData.targetAction}
                  onValueChange={(value) => setFormData({ ...formData, targetAction: value })}
                >
                  <SelectTrigger className="h-12 text-base">
                    <SelectValue placeholder="Выберите действие" />
                  </SelectTrigger>
                  <SelectContent>
                    {mockTargetActions.map((action) => (
                      <SelectItem key={action} value={action}>
                        {action}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Generate Button */}
              <Button
                onClick={handleGenerate}
                disabled={isGenerating}
                className="w-full h-14 text-lg font-semibold bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700 transition-all"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                    Генерация в процессе...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-5 w-5" />
                    Сгенерировать Landing Page
                  </>
                )}
              </Button>
            </div>
          </div>

          {/* Generated Result */}
          {generatedLanding && (
            <div className="bg-white rounded-2xl shadow-xl border border-slate-200 p-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-2xl font-semibold text-slate-800">Ваш Landing Page готов!</h3>
                <div className="flex items-center gap-2 px-4 py-2 bg-green-100 text-green-700 rounded-full">
                  <span className="font-semibold">Lighthouse:</span>
                  <span className="text-xl font-bold">{generatedLanding.lighthouse}/100</span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div className="p-4 bg-slate-50 rounded-lg">
                  <div className="text-sm text-slate-600 mb-1">Тема</div>
                  <div className="font-medium text-slate-900">{generatedLanding.theme}</div>
                </div>
                <div className="p-4 bg-slate-50 rounded-lg">
                  <div className="text-sm text-slate-600 mb-1">Язык</div>
                  <div className="font-medium text-slate-900">{generatedLanding.language}</div>
                </div>
                <div className="p-4 bg-slate-50 rounded-lg">
                  <div className="text-sm text-slate-600 mb-1">Источник трафика</div>
                  <div className="font-medium text-slate-900">{generatedLanding.trafficSource}</div>
                </div>
                <div className="p-4 bg-slate-50 rounded-lg">
                  <div className="text-sm text-slate-600 mb-1">Целевое действие</div>
                  <div className="font-medium text-slate-900">{generatedLanding.targetAction}</div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap gap-4">
                <Button
                  onClick={handlePreview}
                  variant="outline"
                  className="flex-1 h-12 border-2 border-violet-600 text-violet-600 hover:bg-violet-50"
                >
                  <Eye className="mr-2 h-5 w-5" />
                  Предпросмотр
                </Button>
                <Button
                  onClick={() => handleDownload('html')}
                  className="flex-1 h-12 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700"
                >
                  <Download className="mr-2 h-5 w-5" />
                  Скачать HTML
                </Button>
                <Button
                  onClick={() => handleDownload('php')}
                  className="flex-1 h-12 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700"
                >
                  <Download className="mr-2 h-5 w-5" />
                  Скачать PHP
                </Button>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t bg-white mt-20">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-slate-600">
            <p className="mb-2">LandingGen AI - Генератор посадочных страниц премиум-качества</p>
            <p className="text-sm">100/100 Lighthouse • Google Ads Compliant • Anti-AI Resistant</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;