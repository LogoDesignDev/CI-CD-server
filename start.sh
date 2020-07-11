# logo项目前端构建

gitClone() {
    echo "--git clone"
    rm -rf /usr/CI/logo-webui
    git clone --depth=1 https://github.com/LogoDesignDev/logo-webui.git /usr/CI/logo-webui
    echo "success"
}

dependencies() {
    echo "--install dependencies"
    cd /usr/CI/logo-webui
    npm i
    echo "success"
}

build() {
    echo "--build"
    cd /usr/CI/logo-webui
    npm run build
    echo "success"
}

update() {
    echo "--updating"
    cp -rf /usr/CI/logo-webui/dist/. /home/logo-ui
    nginx -s reload
    echo "success"
}

finish() {
    echo "finish."
}

gitClone&&dependencies&&build&&update&&finish
