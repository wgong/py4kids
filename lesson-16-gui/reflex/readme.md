

# Reflex

https://reflex.dev/


## Source
- [reflex](https://github.com/reflex-dev/reflex)
    - ~/projects/UI/reflex/reflex
- [reflex-examples](https://github.com/wgong/reflex-examples)
    - ~/projects/UI/reflex/reflex-examples

## Setup

```
conda create -n reflex python=3.11
conda activate reflex
```

## Features

### AgGrid React component
- https://www.ag-grid.com/react-data-grid/getting-started/
    - https://github.com/orgs/reflex-dev/discussions/3709

- [Wrapping React](https://reflex.dev/docs/wrapping-react/overview/)
- [Custom Components](https://reflex.dev/docs/custom-components/overview/)
    - reflex-spline
    - reflex-webcam
    - reflex-icons
    - color_picker

## News

- [Reflex open source tool helps turn Python code into web apps](https://techcrunch.com/2023/08/02/reflex-open-source-tool-helps-turn-python-code-into-web-apps/)


# Tutorials

## Number Guessing Game (2024-07-28)

https://ai.gopubby.com/reflex-the-framework-to-build-full-stack-web-apps-in-pure-python-e9db479a58ab

see `~/projects/UI/reflex/reflex-examples/guess_number`

## Todo

```
conda activate reflex
cd ~/projects/UI/reflex/reflex-examples
mv todo src_orig
mkdir todo
cd todo
reflex init
export FRONTEND_PORT=3001; reflex run
```

# Resources

## comparisons
https://dev.to/sn3llius/a-quick-comparison-streamlit-dash-reflex-and-rio-57gf 

## Intro:
https://medium.com/@HeCanThink/reflex-a-library-to-build-performant-and-customizable-web-apps-in-pure-python-2bfde0344af2

## Reflex blogs:
https://reflex.dev/blog/2024-03-21-reflex-architecture/
https://reflex.dev/blog/2024-06-28-using-table-component/