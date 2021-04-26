document.addEventListener('DOMContentLoaded', function () {

    M.Dropdown.init(
        document.querySelectorAll('.dropdown-trigger'),
        {
            constrainWidth: false
        }
    );

    // Convert persisted group id array string to actual array
    const persistedChosenGroups = document.getElementById("groups-chosen-input").value.match(/\d+/g)

    for (const groupOption of document.getElementsByClassName("group-option")) {
        groupOption.onclick = () => {
            chooseGroup(groupOption)
        }
        if (persistedChosenGroups != null && persistedChosenGroups.includes(groupOption.dataset.groupId)) {
            chooseGroup(groupOption)
        }
    }

}, false);

/**
 * Add chosen group to collection
 * @param chosenGroupElement dropdown element for chosen group
 */
const chooseGroup = (chosenGroupElement) => {

    const chosenGroup = chosenGroupElement.textContent

    const groupsChosen = document.getElementById("groups-chosen")
    groupsChosen.style.display = "block"

    const groupItem = document.createElement("div")
    groupItem.classList.add("collection-item", "groups-chosen-item")
    groupItem.dataset.groupId = chosenGroupElement.dataset.groupId
    groupItem.value = chosenGroup

    const groupTitle = document.createElement("span")
    groupTitle.className = "groups-chosen-item-title"
    groupTitle.textContent = (groupsChosen.children.length + 1) + ". " + chosenGroup
    groupItem.appendChild(groupTitle)

    const removeButton = document.createElement("span")
    removeButton.className = "material-icons md-24 badge group-option-remove"
    removeButton.textContent = "clear"
    removeButton.onclick = () => {
        groupItem.remove()
        updateChosenGroups()
        updateGroupsPriority()
        if (groupsChosen.children.length === 0) {
            groupsChosen.style.display = "none"
        }
        // Re-enable option to select
        chosenGroupElement.classList.remove("disabled")
    }
    groupItem.appendChild(removeButton)

    groupsChosen.appendChild(groupItem)

    // Disable option from select dropdown (prevent duplicates)
    chosenGroupElement.classList.add("disabled")

    updateChosenGroups()

}

/**
 * Update chosen group items with correct priority numbers
 */
const updateGroupsPriority = () => {

    const groupsChosen = document.getElementById("groups-chosen")
    for (let i = 0; i < groupsChosen.children.length; i++) {
        const group = groupsChosen.children.item(i)
        const groupTitle = group.getElementsByClassName("groups-chosen-item-title")[0]
        groupTitle.textContent = (i + 1) + ". " + group.value
    }

}

/**
 * Update hidden text input field with chosen group ids
 */
const updateChosenGroups = () => {

    let chosenGroupsString = ""

    for (const chosenGroup of document.getElementsByClassName("groups-chosen-item")) {
        const groupId = chosenGroup.dataset.groupId
        if (chosenGroupsString === "") {
            chosenGroupsString = groupId
        } else {
            chosenGroupsString += "," + groupId
        }
    }

    const chosenGroupsInput = document.getElementById("groups-chosen-input")
    chosenGroupsInput.value = chosenGroupsString

}
