#!/bin/sh

DOMAIN='collective.blog.view'

# Synchronise the templates and scripts with the .pot file for collective.blog.view domain.
i18ndude rebuild-pot --pot ./locales/${DOMAIN}.pot \
    --merge ./locales/${DOMAIN}-manual.pot \
    --create ${DOMAIN} \
    ./
    
# Synchronise the collective.blog.view's pot file (Used for the workflows)
i18ndude sync --pot ./locales/${DOMAIN}.pot ./locales/*/LC_MESSAGES/${DOMAIN}.po

# Synchronise the templates and scripts with the .pot file for plone domain.
i18ndude rebuild-pot --pot ./locales/plone.pot \
    --create plone \
    ./profiles/default

# Synchronise the Plone's pot file (Used for the workflows)
for po in ./locales/*/LC_MESSAGES/plone.po; do
    i18ndude sync --pot ./locales/plone.pot $po
done

# Compile po files
for lang in $(find locales -mindepth 1 -maxdepth 1 -type d); do
    if test -d $lang/LC_MESSAGES; then
        msgfmt -o $lang/LC_MESSAGES/${DOMAIN}.mo $lang/LC_MESSAGES/${DOMAIN}.po
        msgfmt -o $lang/LC_MESSAGES/plone.mo $lang/LC_MESSAGES/plone.po
    fi
done

WARNINGS=`find . -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-WARN' | wc -l`
ERRORS=`find . -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-ERROR' | wc -l`
FATAL=`find . -name "*pt"  | xargs i18ndude find-untranslated | grep -e '^-FATAL' | wc -l`

echo
echo "There are $WARNINGS warnings \(possibly missing i18n markup\)"
echo "There are $ERRORS errors \(almost definitely missing i18n markup\)"
echo "There are $FATAL fatal errors \(template could not be parsed, eg. if it\'s not html\)"
echo "For more details, run \'find . -name \"\*pt\" \| xargs i18ndude find-untranslated\' or"
echo "Look the rebuild i18n log generate for this script called \'rebuild_i18n.log\' on locales dir"

rm ./i18n.log

touch ./i18n.log

find ./ -name "*pt" | xargs i18ndude find-untranslated > i18n.log
