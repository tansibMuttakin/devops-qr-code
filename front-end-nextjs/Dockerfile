FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json yarn.lock* /app/

RUN \
    if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    elif [ -f pnpm-lock.yamml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
    else echo "Lockfile not found." && exit 1; \
    fi

COPY . /app

RUN npm run build

EXPOSE 8080

CMD ["npm", "run", "start","--", "-p", "8080"]