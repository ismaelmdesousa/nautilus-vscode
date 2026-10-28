# nautilus-vscode

[English](README.md) | **Português brasileiro**

Extensão do Nautilus (Arquivos do GNOME) que adiciona **Abrir no VS Code**
ao menu do botão direito de uma pasta e ao menu da área vazia da pasta atual.
Abre a pasta em uma nova janela do Visual Studio Code.

## Requisitos

- Debian com GNOME e Nautilus 43 ou superior.
- Visual Studio Code com o comando `code` disponível no ambiente do Nautilus.
- Suporte a extensões Python do Nautilus:

```bash
sudo apt install python3-nautilus
```

Confira se o comando do editor está disponível:

```bash
command -v code
```

A extensão funciona com pastas locais. Pastas remotas, como endereços
`smb://` e `sftp://`, não exibem a opção.

## Ambiente testado

O autor testou manualmente a instalação global em
`/usr/share/nautilus-python/extensions/` no seguinte ambiente:

| Componente | Versão |
| --- | --- |
| Debian GNU/Linux | 13.7 (trixie) |
| GNOME Shell | 48.7 |
| Nautilus (Arquivos) | 48.3 |
| python3-nautilus | 4.0.1 |

As versões foram consultadas nos metadados do sistema e nos pacotes
instalados no ambiente atual de teste.

## Instalação

Execute os comandos a partir da pasta deste repositório. Escolha apenas uma
das opções abaixo para evitar carregar duas cópias da extensão.
Não é necessário tornar o arquivo Python executável.

### Compilar as traduções

Instale a ferramenta e compile todos os catálogos antes de copiar os arquivos:

```bash
sudo apt install gettext
for catalog in po/*.po; do
    language=$(basename "$catalog" .po)
    mkdir -p "locale/$language/LC_MESSAGES"
    msgfmt --check "$catalog" -o "locale/$language/LC_MESSAGES/nautilus-vscode.mo"
done
```

### Somente para o usuário atual

O diretório padrão é `~/.local/share/nautilus-python/extensions/`.
Se `XDG_DATA_HOME` estiver definido, utilize-o no lugar de `~/.local/share`.

```bash
install -Dm644 nautilus-vscode.py "${XDG_DATA_HOME:-$HOME/.local/share}/nautilus-python/extensions/nautilus-vscode.py"
for catalog in po/*.po; do
    language=$(basename "$catalog" .po)
    install -Dm644 "locale/$language/LC_MESSAGES/nautilus-vscode.mo" "${XDG_DATA_HOME:-$HOME/.local/share}/nautilus-python/extensions/locale/$language/LC_MESSAGES/nautilus-vscode.mo"
done
```

### Global, para todos os usuários

No Debian, instale em `/usr/share/nautilus-python/extensions/`:

```bash
sudo install -Dm644 nautilus-vscode.py /usr/share/nautilus-python/extensions/nautilus-vscode.py
for catalog in po/*.po; do
    language=$(basename "$catalog" .po)
    sudo install -Dm644 "locale/$language/LC_MESSAGES/nautilus-vscode.mo" "/usr/share/nautilus-python/extensions/locale/$language/LC_MESSAGES/nautilus-vscode.mo"
done
```

A instalação global foi testada manualmente pelo autor no GNOME/Nautilus.
Cada usuário precisa ter acesso ao comando `code` em sua sessão.

### Carregar a extensão

Após instalar ou atualizar, encerre o Nautilus:

```bash
nautilus -q
```

Abra novamente o aplicativo **Arquivos**. Na instalação global, cada usuário
precisa reiniciar o próprio Nautilus para carregar a extensão.

## Uso e verificação

1. Clique com o botão direito em uma pasta local.
2. Escolha **Abrir no VS Code** e confira se a pasta abre em uma nova janela.
3. Entre em uma pasta, clique com o botão direito numa área vazia e repita.

A opção aparece quando uma única pasta está selecionada ou no menu da área
vazia. Ela não aparece para arquivos ou para várias pastas selecionadas.
A posição do item é definida pelo Nautilus.

A extensão não altera o aplicativo padrão de pastas nem depende de uma
associação do VS Code ao tipo MIME `inode/directory`.

## Atualização

Compile novamente as traduções e copie o `.py` e o `.mo` usando os comandos
da instalação escolhida. Reinicie o Nautilus com `nautilus -q`.

## Remoção

### Instalação do usuário

```bash
rm -- "${XDG_DATA_HOME:-$HOME/.local/share}/nautilus-python/extensions/nautilus-vscode.py"
for catalog in po/*.po; do
    language=$(basename "$catalog" .po)
    rm -f -- "${XDG_DATA_HOME:-$HOME/.local/share}/nautilus-python/extensions/locale/$language/LC_MESSAGES/nautilus-vscode.mo"
done
nautilus -q
```

### Instalação global

```bash
sudo rm -- /usr/share/nautilus-python/extensions/nautilus-vscode.py
for catalog in po/*.po; do
    language=$(basename "$catalog" .po)
    sudo rm -f -- "/usr/share/nautilus-python/extensions/locale/$language/LC_MESSAGES/nautilus-vscode.mo"
done
nautilus -q
```

## Solução de problemas

Se a opção não aparecer, confira se `python3-nautilus` está instalado,
se o arquivo foi copiado para o diretório escolhido e se o Nautilus foi
reiniciado. Confirme também que a pasta é local.

Se a opção aparecer, mas o editor não abrir, teste no terminal:

```bash
code --new-window /caminho/da/pasta
```

Se o comando funcionar apenas por meio de um alias ou de uma configuração do
shell, disponibilize o executável `code` no `PATH` da sessão gráfica.

## Idiomas e tradução

O `gettext` seleciona a tradução conforme o ambiente do processo do Nautilus,
consultando `LANGUAGE`, `LC_ALL`, `LC_MESSAGES` e `LANG`, nessa ordem.
O idioma original é inglês. Estão disponíveis os seguintes catálogos:

| Idioma | Catálogo |
| --- | --- |
| Árabe | `ar` |
| Bengali | `bn` |
| Português brasileiro | `pt_BR` |
| Francês | `fr` |
| Hindi | `hi` |
| Indonésio | `id` |
| Chinês simplificado (mandarim) | `zh_CN` |
| Espanhol | `es` |
| Urdu | `ur` |

Sem um catálogo disponível para o idioma selecionado, o menu aparece em inglês.
Após mudar o idioma da sessão, reinicie o Nautilus para recarregar a tradução.

Os arquivos `po/*.po` contêm as traduções editáveis. Os arquivos `.mo` são
catálogos compilados e devem ser instalados na pasta `locale` ao lado da
extensão. Eles são gerados localmente e ignorados pelo Git.

Para adicionar um idioma, extraia as mensagens e crie o catálogo (exemplo
para alemão):

```bash
xgettext --language=Python --from-code=UTF-8 --keyword=_ --package-name=nautilus-vscode -o /tmp/nautilus-vscode.pot nautilus-vscode.py
msginit --no-translator --locale=de --input=/tmp/nautilus-vscode.pot --output-file=po/de.po
```

Traduza os campos `msgstr` de `po/de.po`, compile com `msgfmt --check` e
instale em `locale/de/LC_MESSAGES/nautilus-vscode.mo`, seguindo os mesmos
passos de instalação dos catálogos existentes.

## Validação de desenvolvimento

Para validar a sintaxe sem abrir o editor:

```bash
python3 -m py_compile nautilus-vscode.py
git diff --check
```

Essa verificação não substitui o teste manual do menu no Nautilus.

## Documentação

Consulte o [manual oficial do nautilus-python](https://gnome.pages.gitlab.gnome.org/nautilus-python/) para a API de
extensões, incluindo `Nautilus.MenuProvider` e `Nautilus.MenuItem`.

## Licença

MIT, conforme o arquivo [LICENSE](LICENSE). O texto completo da licença também
está no cabeçalho de `nautilus-vscode.py`, para acompanhar instalações que
copiem apenas esse arquivo. Não é necessário instalar `LICENSE` separadamente
nos diretórios de extensões.
